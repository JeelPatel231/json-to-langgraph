from core.context.global_context import AuthenticatedUser, DbConnection, GlobalContext
from core.engine.types import GenericState
from core.engine.serializer import JsonToGraphSerializer
from core.engine.unions import WorkflowSpec


def main():
    with open("workflow.json", "r") as f:
        json = f.read()

    workflow_spec = WorkflowSpec.model_validate_json(json)

    global_context = GlobalContext(
        db_connection=DbConnection(),
        current_user=AuthenticatedUser(),
    )

    serializer = JsonToGraphSerializer(global_context)
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
