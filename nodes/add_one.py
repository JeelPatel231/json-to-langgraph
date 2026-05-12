from pydantic import BaseModel

from core.types import GenericState
from .utils import pydantic_args


class AddOneArgs(BaseModel):
    a: int


@pydantic_args
def add_one(args: AddOneArgs, state: GenericState) -> int:
    return args.a + 1
