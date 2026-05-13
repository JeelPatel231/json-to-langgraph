from typing import Annotated, Literal
from pydantic import BaseModel, Field

from core.context.global_context import GlobalContext
from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseExecutableNode


class TakeInputParams(BaseModel):
    prompt: Annotated[str, CEL] = Field("Enter a value: ")


class TakeInputNode(BaseExecutableNode[TakeInputParams, None]):
    name: Literal["take_input"] = "take_input"
    config: None = None

    def __call__(
        self,
        params: TakeInputParams,
        state: GenericState,
        config: None,
        *,
        global_context: GlobalContext,
    ):
        return input(params.prompt)
