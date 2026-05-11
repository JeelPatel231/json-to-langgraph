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
                        destination="if_small",
                        condition=CommonExpression(expr="nodes.test_node < 2"),
                    ),
                    Transition(
                        destination="if_big",
                        condition=CommonExpression(expr="nodes.test_node >= 2"),
                    ),
                ],
            ),
            Node(
                id="if_small",
                type=ExecutableNode(
                    guid="if_small",
                    input={"a": CommonExpression(expr="nodes.test_node")},
                    callback=lambda _input, state: _input["a"] + 5,
                ),
                transitions=[
                    Transition(
                        destination=END,
                    )
                ],
            ),
            Node(
                id="if_big",
                type=ExecutableNode(
                    guid="if_big",
                    input={"a": CommonExpression(expr="nodes.test_node")},
                    callback=lambda _input, state: _input["a"] + 100,
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

    a = realised_workflow.compile().invoke(GenericState(input={"a": 0}))
    print(a)


if __name__ == "__main__":
    main()
