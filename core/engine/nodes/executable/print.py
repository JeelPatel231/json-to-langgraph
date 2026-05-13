from typing import Annotated, Literal
from pydantic import BaseModel

from core.context.global_context import GlobalContext
from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseExecutableNode


class PrintArgs(BaseModel):
    text: Annotated[str, CEL]


class PrintNode(BaseExecutableNode[PrintArgs, None]):
    name: Literal["print"] = "print"
    config: None = None

    def __call__(
        self,
        params: PrintArgs,
        state: GenericState,
        config: None,
        *,
        global_context: GlobalContext,
    ):
        print(params.text)
