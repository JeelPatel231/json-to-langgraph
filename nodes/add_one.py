from pydantic import BaseModel

from core.types import GenericState, global_node_registry
from .utils import pydantic_args


class AddOneArgs(BaseModel):
    a: int

@global_node_registry.register_decorator()
@pydantic_args
def add_one(args: AddOneArgs, state: GenericState) -> int:
    return args.a + 1
