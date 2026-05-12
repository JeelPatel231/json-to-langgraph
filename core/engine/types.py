from typing import Literal
from typing import Annotated
from core.engine.cel import CEL, CommonExpression
from core.engine.state import GenericState
from typing import TypeAliasType
from pydantic.fields import Field
from pydantic import BaseModel

NodeInput = TypeAliasType("NodeInput", dict[str, "CommonExpression | NodeInput"])
NodeConfig = dict[str, str]


class Transition(BaseModel):
    destination: str
    condition: CommonExpression = Field(
        default_factory=lambda: CommonExpression("true")
    )


class BaseNodeModel[T](BaseModel):
    id: T
    transitions: list[Transition] = Field(default_factory=list)
