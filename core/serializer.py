from core.types import ExecutableNode
from core.types import Transition
from langgraph.graph import StateGraph
from core.types import WorkflowSpec, GenericState
import cel


class ExpressionEvalRouter:
    def __init__(self, transitions: list[Transition]):
        self.transitions = transitions

    def __call__(self, state: GenericState) -> str:
        next_routes = []
        for transition in self.transitions:
            # TODO: the state is still pending to be built. Try to keep it as generic as possible.
            if cel.evaluate(transition.condition.expr, {"state": state.model_dump()}):
                next_routes.append(transition.destination)
        return next_routes


class JsonToGraphSerializer:
    def serialize(self, workflow_spec: WorkflowSpec) -> StateGraph:
        workflow = StateGraph(GenericState)

        for node in workflow_spec.nodes:
            if isinstance(node.type, ExecutableNode):
                runner = node.type.callback
                workflow.add_node(node.id, runner)

            for transition in node.transitions:
                router = ExpressionEvalRouter(node.transitions)
                workflow.add_conditional_edges(node.id, router)

        return workflow
