from core.engine.types import GenericState, WorkflowSpec
from core.engine.serializer import JsonToGraphSerializer


def main():
    with open("workflow.json", "r") as f:
        json = f.read()

    workflow_spec = WorkflowSpec.model_validate_json(json)

    serializer = JsonToGraphSerializer()
    realised_workflow = serializer.serialize(workflow_spec)

    runner = realised_workflow.compile()

    print(
        runner.invoke(
            GenericState(
                input={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Hello"}],
                }
            )
        )
    )


if __name__ == "__main__":
    main()
