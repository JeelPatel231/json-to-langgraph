from core.engine.types import GenericState


def print_node(args: dict[str, None], state: GenericState):
    print("[PRINT_NODE]", {"state": state, "args": args})
