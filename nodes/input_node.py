from core.types import GenericState, global_node_registry

@global_node_registry.register_decorator()
def take_input(args: dict[str, None], state: GenericState) -> str:
    return input("Enter input: ")
