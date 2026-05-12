from pydantic import BaseModel, Field
from typing import Any


class GenericState(BaseModel):
    input: dict[str, Any] = Field(default_factory=dict)
    nodes: dict[str, Any] = Field(default_factory=dict)
