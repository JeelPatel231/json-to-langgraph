from __future__ import annotations

from typing import Literal
from typing import Annotated
from core.engine.state import GenericState
from typing import Sequence
from typing import TypeAliasType
from typing import Callable
from typing import Any
from pydantic.fields import Field
from pydantic import field_validator
from pydantic import BaseModel
from pydantic import RootModel
import cel


class CommonExpression(RootModel[str]):
    root: str = "true"

    @field_validator("root")
    @classmethod
    def validate_expression(cls, v: str):
        cel.compile(v)
        return v

    @property
    def expr(self) -> str:
        return self.root


NodeInput = TypeAliasType("NodeInput", dict[str, "CommonExpression | NodeInput"])
NodeConfig = dict[str, str]

ExecutableNodeFunction = Callable[[dict[str, Any], GenericState], Any]


class NodeRegistry:
    def __init__(self):
        self._registry: dict[str, ExecutableNodeFunction] = {}

    def list_nodes(self) -> list[str]:
        return list(self._registry.keys())

    def register(self, guid: str, func: ExecutableNodeFunction):
        self._registry[guid] = func

    def register_all(
        self,
        modules: Sequence[tuple[str, ExecutableNodeFunction] | ExecutableNodeFunction],
    ):
        for node in modules:
            if isinstance(node, tuple):
                self.register(node[0], node[1])
            else:
                self.register(node.__name__, node)

    def __contains__(self, guid: str) -> bool:
        return guid in self._registry

    def get(self, guid: str) -> ExecutableNodeFunction:
        callable_func = self._registry.get(guid)
        if not callable_func:
            raise ValueError(
                f"Node with name '{guid}' not found in registry. Available nodes: {self.list_nodes()}"
            )
        return self._registry[guid]


global_node_registry = NodeRegistry()


class Transition(BaseModel):
    destination: str
    condition: CommonExpression = Field(default_factory=lambda: CommonExpression())


class WorkflowSpec(BaseModel):
    name: str
    nodes: list[Node]


# =========


class BaseNodeModel(BaseModel):
    id: str
    type: str
    transitions: list[Transition] = Field(default_factory=list)


class TakeInputParams(BaseModel):
    non_default_param: int
    prompt: str = Field("Enter a value: ")


class BaseExecutableNode(BaseNodeModel):
    id: str
    type: Literal["executable"] = "executable"


class TakeInputNode(BaseExecutableNode):
    name: Literal["take_input"] = "take_input"
    input: TakeInputParams = Field(default_factory=lambda: TakeInputParams())

    def __call__(self, params: TakeInputParams, state: GenericState):
        print(params.non_default_param)
        return input(params.prompt)


class MarkerNode(BaseNodeModel):
    type: Literal["marker"] = "marker"


class StartNode(MarkerNode):
    id: Literal["__start__"] = "__start__"


class EndNode(MarkerNode):
    id: Literal["__end__"] = "__end__"


MarkerNode = Annotated[StartNode | EndNode, Field(discriminator="id")]

ExecutableNode = Annotated[TakeInputNode, Field(discriminator="name")]

Node = MarkerNode | ExecutableNode
