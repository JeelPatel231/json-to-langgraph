from __future__ import annotations

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
    condition: CommonExpression = Field(default_factory=lambda: CommonExpression("true"))

# =========


class BaseNodeModel[T](BaseModel):
    id: T
    transitions: list[Transition] = Field(default_factory=list)

class TakeInputParams(BaseModel):
    prompt: Annotated[str, CEL] = Field("Enter a value: ")


class BaseExecutableNode[T: BaseModel](BaseNodeModel[str]):
    type: Literal["executable"] = "executable"
    input: T

    def __call__(self, params: T, state: GenericState):
        raise NotImplementedError("Executable nodes must implement the __call__ method.")

class TakeInputNode(BaseExecutableNode[TakeInputParams]):
    name: Literal["take_input"] = "take_input"

    def __call__(self, params: TakeInputParams, state: GenericState):
        return input(params.prompt)

class PrintArgs(BaseModel):
    text: Annotated[str, CEL]

class PrintNode(BaseExecutableNode[PrintArgs]):
    name: Literal["print"] = "print"

    def __call__(self, params: PrintArgs, state: GenericState):
        print(params.text)

class BaseMarkerNode(BaseNodeModel):
    type: Literal["marker"] = "marker"


class StartNode(BaseMarkerNode):
    id: Literal["__start__"] = "__start__"


class EndNode(BaseMarkerNode):
    id: Literal["__end__"] = "__end__"


MarkerNode = Annotated[StartNode | EndNode, Field(discriminator="id")]

ExecutableNode = Annotated[TakeInputNode | PrintNode, Field(discriminator="name")]

Node = MarkerNode | ExecutableNode

# ==============

class WorkflowSpec(BaseModel):
    name: str
    nodes: list[Node]

