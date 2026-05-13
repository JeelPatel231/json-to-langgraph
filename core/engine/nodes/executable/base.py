from typing import Literal
from pydantic import BaseModel

from core.context.global_context import GlobalContext
from core.engine.state import GenericState
from core.engine.types import BaseNodeModel


class BaseExecutableNode[T: BaseModel, U: BaseModel | None](BaseNodeModel[str]):
    type: Literal["executable"] = "executable"
    input: T
    config: U

    def __call__(
        self,
        params: T,
        state: GenericState,
        config: U,
        *,
        global_context: GlobalContext,
    ):
        raise NotImplementedError(
            "Executable nodes must implement the __call__ method."
        )
