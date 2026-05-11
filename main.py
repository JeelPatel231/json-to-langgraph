from langgraph.constants import END
from langgraph.constants import START
from core.types import MarkerNode
from core.serializer import JsonToGraphSerializer
from core.types import CommonExpression
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
                        condition=CommonExpression(expr="true"),
                    )
                ],
            ),
            Node(
                id="test_node",
                type=ExecutableNode(
                    guid="test_node", callback=lambda state: print("test_node")
                ),
                transitions=[
                    Transition(
                        destination="test_node_2",
                        condition=CommonExpression(expr="1"),
                    )
                ],
            ),
            Node(
                id="test_node_2",
                type=ExecutableNode(
                    guid="test_node_2", callback=lambda state: print("test_node_2")
                ),
                transitions=[
                    Transition(
                        destination=END,
                        condition=CommonExpression(expr="true"),
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

    a = realised_workflow.compile().invoke({})
    print(a)


if __name__ == "__main__":
    main()
