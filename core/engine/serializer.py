from core.engine.nodes.executable.base import (
    BaseConfigurableExecutableNode,
    BaseExecutableNode,
)
from core.engine.unions import WorkflowSpec

from core.engine.types import Transition
from pydantic import BaseModel
from langgraph.graph import StateGraph
from core.engine.cel import CommonExpression
from core.engine.types import GenericState
import cel


class ExpressionEvalRouter:
    def __init__(self, transitions: list[Transition]):
        self.transitions = transitions

    def __call__(self, state: GenericState) -> list[str]:
        next_routes: list[str] = []
        for transition in self.transitions:
            if cel.evaluate(transition.condition.expr, state.model_dump()):
                next_routes.append(transition.destination)
        return next_routes


def evaluate_node_inputs_recursive(node_inputs: BaseModel, state: GenericState):
    transformed = dict()
    for key, value in node_inputs:
        if isinstance(value, CommonExpression):
            _dumped = state.model_dump()
            transformed[key] = cel.evaluate(value.expr, _dumped)
        elif isinstance(value, BaseModel):
            transformed[key] = evaluate_node_inputs_recursive(value, state)
        else:
            raise Exception(f"Invalid type {type(value)} for {key}")
    return transformed


class ExecutionNodeCallableWrapper[T: BaseModel]:
    def __init__(self, node: BaseExecutableNode[T]):
        self.node = node

    def __call__(self, state: GenericState):
        # grabs the model, takes out all the fields and evaluates them recursively
        evaluated_inputs = evaluate_node_inputs_recursive(self.node.input, state)

        validated_input = self.node.input.model_validate(
            evaluated_inputs, context={"cel_mode": False}
        )

        # create a pydantic model from the evaluated fields and pass them to the callback.
        node_output = self.node(validated_input, state)

        # store the output of the node in the state
        state.nodes[self.node.id] = node_output
        return state


class ConfigurableExecutionNodeCallableWrapper[T: BaseModel, U: BaseModel]:
    def __init__(self, node: BaseConfigurableExecutableNode[T, U]):
        self.node = node

    def __call__(self, state: GenericState):
        # grabs the model, takes out all the fields and evaluates them recursively
        evaluated_inputs = evaluate_node_inputs_recursive(self.node.input, state)
        validated_input = self.node.input.model_validate(
            evaluated_inputs, context={"cel_mode": False}
        )

        evaluated_config = evaluate_node_inputs_recursive(self.node.config, state)
        validated_config = self.node.config.model_validate(
            evaluated_config, context={"cel_mode": False}
        )
        # TODO: there may be some adapter code to be called here for db access and the like, but for now we can just pass the config to the node directly.
        
        # create a pydantic model from the evaluated fields and pass them to the callback.
        node_output = self.node(validated_input, state, validated_config)

        # store the output of the node in the state
        state.nodes[self.node.id] = node_output
        return state


class JsonToGraphSerializer:
    def serialize(self, workflow_spec: WorkflowSpec) -> StateGraph:
        workflow = StateGraph(GenericState)

        for node in workflow_spec.nodes:
            if isinstance(node, BaseExecutableNode):
                wrapper = ExecutionNodeCallableWrapper(node)
                workflow.add_node(node.id, wrapper)

            elif isinstance(node, BaseConfigurableExecutableNode):
                wrapper = ConfigurableExecutionNodeCallableWrapper(node)
                workflow.add_node(node.id, wrapper)

            if node.transitions:
                router = ExpressionEvalRouter(node.transitions)
                destinations = [t.destination for t in node.transitions]
                workflow.add_conditional_edges(node.id, router, path_map=destinations)

        return workflow
