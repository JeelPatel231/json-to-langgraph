from typing import Annotated, Literal
from pydantic import BaseModel

from core.context.global_context import GlobalContext
from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseExecutableNode


class APICallerParams(BaseModel):
    endpoint: Annotated[str, CEL]


class APICallerConfig(BaseModel):
    timeout: Annotated[int, CEL]


class APICallerNode(BaseExecutableNode[APICallerParams, APICallerConfig]):
    name: Literal["api_caller"] = "api_caller"

    def __call__(
        self,
        params: APICallerParams,
        state: GenericState,
        config: APICallerConfig,
        *,
        global_context: GlobalContext,
    ):
        print("Configuration", config)
        print("Global Context", global_context)
        # Placeholder implementation - replace with actual API call logic
        return f"API call to {params.endpoint}"
