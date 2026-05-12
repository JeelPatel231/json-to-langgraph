from typing import Literal
from pydantic import BaseModel

from core.engine.state import GenericState
from core.engine.types import BaseNodeModel


class BaseExecutableNode[T: BaseModel](BaseNodeModel[str]):
    type: Literal["executable"] = "executable"
    input: T

    def __call__(self, params: T, state: GenericState):
        raise NotImplementedError(
            "Executable nodes must implement the __call__ method."
        )
