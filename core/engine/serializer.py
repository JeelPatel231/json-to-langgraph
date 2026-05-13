from core.context.global_context import GlobalContext
from core.engine.nodes.executable.base import BaseExecutableNode
from core.engine.unions import WorkflowSpec

from core.engine.types import Transition
from pydantic import BaseModel
from langgraph.graph import StateGraph
from core.engine.cel import CommonExpression
from core.engine.state import GenericState
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


class ExecutionNodeCallableWrapper[T: BaseModel, U: BaseModel]:
    def __init__(self, node: BaseExecutableNode[T, U], global_context: GlobalContext):
        self.__node = node
        self.__global_context = global_context

    def __call__(self, state: GenericState):
        # grabs the model, takes out all the fields and evaluates them recursively
        evaluated_inputs = evaluate_node_inputs_recursive(self.__node.input, state)
        validated_input = self.__node.input.model_validate(
            evaluated_inputs, context={"cel_mode": False}
        )

        validated_config = None
        if self.__node.config is not None:
            evaluated_config = evaluate_node_inputs_recursive(self.__node.config, state)
            validated_config = self.__node.config.model_validate(
                evaluated_config, context={"cel_mode": False}
            )

        # create a pydantic model from the evaluated fields and pass them to the callback.
        node_output = self.__node(
            params=validated_input,
            state=state,
            config=validated_config,
            global_context=self.__global_context,
        )

        # store the output of the node in the state
        state.nodes[self.__node.id] = node_output
        return state


class JsonToGraphSerializer:
    def __init__(self, global_context: GlobalContext):
        self.__global_context = global_context

    def serialize(self, workflow_spec: WorkflowSpec) -> StateGraph:
        workflow = StateGraph(GenericState)

        for node in workflow_spec.nodes:
            if isinstance(node, BaseExecutableNode):
                wrapper = ExecutionNodeCallableWrapper(node, self.__global_context)
                workflow.add_node(node.id, wrapper)

            if node.transitions:
                router = ExpressionEvalRouter(node.transitions)
                destinations = [t.destination for t in node.transitions]
                workflow.add_conditional_edges(node.id, router, path_map=destinations)

        return workflow
