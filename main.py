from core.types import GenericState
from core.types import CommonExpression
from langgraph.constants import END
from langgraph.constants import START
from core.types import MarkerNode
from core.serializer import JsonToGraphSerializer
from core.types import Transition
from core.types import ExecutableNode
from core.types import Node
from core.types import WorkflowSpec


def main():
    workflow_spec = WorkflowSpec(
        name="test_workflow",
        nodes=[
            Node(
                id=START,
                type=MarkerNode(),
                transitions=[
                    Transition(
                        destination="test_node",
                    )
                ],
            ),
            Node(
                id="test_node",
                type=ExecutableNode(
                    guid="test_node",
                    input={"a": CommonExpression(expr='input["a"]')},
                    callback=lambda _input, state: _input["a"] + 1,
                ),
                transitions=[
                    Transition(
                        destination="test_node_2",
                    )
                ],
            ),
            Node(
                id="test_node_2",
                type=ExecutableNode(
                    guid="test_node_2",
                    input={"b": CommonExpression(expr='input["a"] + 1')},
                    callback=lambda _input, state: _input["b"] + 2,
                ),
                transitions=[
                    Transition(
                        destination=END,
                    )
                ],
            ),
            Node(
                id=END,
                type=MarkerNode(),
                transitions=[],
            ),
        ],
    )

    serializer = JsonToGraphSerializer()
    realised_workflow = serializer.serialize(workflow_spec)

    a = realised_workflow.compile().invoke(GenericState(input={"a": 1}))
    print(a["nodes"])


if __name__ == "__main__":
    main()
