from typing import Annotated, Literal
from pydantic import BaseModel, Field

from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseExecutableNode


class APICallerParams(BaseModel):
    endpoint: Annotated[str, CEL]

class APICallerConfig(BaseModel):
    timeout: int

class APICallerNode(BaseExecutableNode[APICallerParams]):
    name: Literal["api_caller"] = "api_caller"

    config: APICallerConfig

    def __call__(self, params: APICallerParams, state: GenericState):
        print('Configuration', self.config)
        # Placeholder implementation - replace with actual API call logic
        return f"API call to {params.endpoint}"
