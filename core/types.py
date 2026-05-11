from typing import Annotated
from typing import Literal
from langgraph.typing import StateLike
from typing import Callable
from typing import Any
from dataclasses import field
from pydantic.fields import Field
from pydantic import field_validator
from dataclasses import dataclass
from pydantic import BaseModel
import cel


class CommonExpression(BaseModel):
    expr: str = Field("true", description="CEL expression to evaluate")

    @field_validator("expr")
    def validate_expression(cls, v: str):
        cel.compile(v)
        return v


# these already exist in the graph
class MarkerNode(BaseModel):
    type: Literal["marker"] = field(default="marker", init=False)


NodeInput = dict[str, "CommonExpression | NodeInput"]

# TODO: check if a node can return anything or does it just update the graph state and be done with it.
ExecutableNodeFunction = Callable[[dict[str, Any], StateLike], dict[str, Any]]


@dataclass(frozen=True)
class ExecutableNode:
    type: Literal["executable"] = field(default="executable", init=False)
    guid: str
    callback: ExecutableNodeFunction
    input: NodeInput = field(default_factory=dict)


@dataclass
class Transition:
    destination: str
    condition: CommonExpression = field(default_factory=CommonExpression)


@dataclass
class Node:
    id: str
    object: Annotated[ExecutableNode | MarkerNode, Field(discriminator="type")]
    transitions: list[Transition]


@dataclass
class WorkflowSpec:
    name: str
    nodes: list[Node]


class GenericState(BaseModel):
    input: dict[str, Any] = field(default_factory=dict)
    nodes: dict[str, Any] = field(default_factory=dict)
