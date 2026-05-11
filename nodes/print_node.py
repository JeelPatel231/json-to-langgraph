from core.types import GenericState, global_node_registry


@global_node_registry.register_decorator()
def print_node(args: dict[str, None], state: GenericState):
    print('[PRINT_NODE]', {"state": state, "args": args})
