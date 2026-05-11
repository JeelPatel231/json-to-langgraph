from pydantic import field_validator
from dataclasses import dataclass
from langgraph.typing import ContextT
from langgraph.typing import NodeInputT
from langgraph.graph import StateNode
from pydantic import BaseModel
import cel


class CommonExpression(BaseModel):
    expr: str

    @field_validator("expr")
    def validate_expression(cls, v: str):
        cel.compile(v)
        return v

@dataclass(frozen=True)
class ExecutableNode:
    guid: str
    callback: StateNode[NodeInputT, ContextT]

class Transition(BaseModel):
    destination: str
    condition: CommonExpression

class Node(BaseModel):
    id: str
    type: ExecutableNode
    transitions: list[Transition]

class WorkflowSpec(BaseModel):
    name: str
    nodes: list[Node]

class GenericState(BaseModel):
    ...