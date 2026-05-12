from typing import Annotated, Literal
from pydantic import BaseModel

from core.engine.cel import CEL
from core.engine.state import GenericState
from .base import BaseConfigurableExecutableNode


class APICallerParams(BaseModel):
    endpoint: Annotated[str, CEL]

class APICallerConfig(BaseModel):
    timeout: Annotated[int, CEL]

class APICallerNode(BaseConfigurableExecutableNode[APICallerParams, APICallerConfig]):
    name: Literal["api_caller"] = "api_caller"

    def __call__(self, params: APICallerParams, state: GenericState, config: APICallerConfig):
        print('Configuration', config)
        # Placeholder implementation - replace with actual API call logic
        return f"API call to {params.endpoint}"
