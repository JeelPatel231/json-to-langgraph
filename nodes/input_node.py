from core.engine.types import GenericState


def take_input(args: dict[str, None], state: GenericState) -> str:
    return input("Enter input: ")
