from core.types import GenericState
from core.serializer import JsonToGraphSerializer
from core.types import WorkflowSpec, global_node_registry
import nodes

global_node_registry.register_all(nodes.__all__)


def main():
    with open("workflow.json", "r") as f:
        json = f.read()

    workflow_spec = WorkflowSpec.model_validate_json(json)

    serializer = JsonToGraphSerializer()
    realised_workflow = serializer.serialize(workflow_spec)

    runner = realised_workflow.compile()

    print(runner.invoke(GenericState(input={"a": 0})))

    print(runner.invoke(GenericState(input={"a": 1})))


if __name__ == "__main__":
    main()
