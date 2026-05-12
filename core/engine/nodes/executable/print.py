from typing import Annotated, Literal
from pydantic import BaseModel

from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseExecutableNode


class PrintArgs(BaseModel):
    text: Annotated[str, CEL]


class PrintNode(BaseExecutableNode[PrintArgs]):
    name: Literal["print"] = "print"

    def __call__(self, params: PrintArgs, state: GenericState):
        print(params.text)
