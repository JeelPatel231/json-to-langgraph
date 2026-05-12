from typing import Annotated, Literal
from pydantic import BaseModel, Field

from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseExecutableNode


class TakeInputParams(BaseModel):
    prompt: Annotated[str, CEL] = Field("Enter a value: ")


class TakeInputNode(BaseExecutableNode[TakeInputParams]):
    name: Literal["take_input"] = "take_input"

    def __call__(self, params: TakeInputParams, state: GenericState):
        return input(params.prompt)
