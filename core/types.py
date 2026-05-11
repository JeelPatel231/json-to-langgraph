from dataclasses import field
from langgraph.graph._node import StateNode
from pydantic.fields import Field
from pydantic import field_validator
from dataclasses import dataclass
from langgraph.typing import ContextT
from langgraph.typing import NodeInputT
from pydantic import BaseModel
import cel


class CommonExpression(BaseModel):
    expr: str = Field("true", description="CEL expression to evaluate")

    @field_validator("expr")
    def validate_expression(cls, v: str):
        cel.compile(v)
        return v


# these already exist in the graph
class MarkerNode(BaseModel): ...


@dataclass(frozen=True)
class ExecutableNode:
    guid: str
    callback: StateNode[NodeInputT, ContextT]
    # TODO: input schema


@dataclass
class Transition:
    destination: str
    condition: CommonExpression = field(default_factory=CommonExpression)


@dataclass
class Node:
    id: str
    type: ExecutableNode | MarkerNode
    transitions: list[Transition]


@dataclass
class WorkflowSpec:
    name: str
    nodes: list[Node]


class GenericState(BaseModel): ...
