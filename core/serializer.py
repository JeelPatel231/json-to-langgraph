from core.types import Node
from core.types import ExecutableNodeFunction
from core.types import CommonExpression
from core.types import NodeInput
from core.types import ExecutableNode
from core.types import Transition
from langgraph.graph import StateGraph
from core.types import WorkflowSpec, GenericState
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


def evaluate_node_inputs_recursive(node_inputs: NodeInput, state: GenericState):
    transformed = dict()
    for key, value in node_inputs.items():
        if isinstance(value, CommonExpression):
            _dumped = state.model_dump()
            transformed[key] = cel.evaluate(value.expr, _dumped)
        elif isinstance(value, dict):
            transformed[key] = evaluate_node_inputs_recursive(value, state)
        else:
            raise Exception(f"Invalid type {type(value)} for {key}")
    return transformed


class ExecutionNodeCallableWrapper:
    def __init__(self, node: Node):
        assert isinstance(node.type, ExecutableNode)
        self.node = node

    def __call__(self, state: GenericState):
        evaluated_inputs = evaluate_node_inputs_recursive(self.node.type.input, state)
        node_output = self.node.type.callback(evaluated_inputs, state)
        state.nodes[self.node.id] = node_output
        return state


class JsonToGraphSerializer:
    def serialize(self, workflow_spec: WorkflowSpec) -> StateGraph:
        workflow = StateGraph(GenericState)

        for node in workflow_spec.nodes:
            if isinstance(node.type, ExecutableNode):
                wrapper = ExecutionNodeCallableWrapper(node)
                workflow.add_node(node.id, wrapper)

            if node.transitions:
                router = ExpressionEvalRouter(node.transitions)
                workflow.add_conditional_edges(node.id, router)

        return workflow
