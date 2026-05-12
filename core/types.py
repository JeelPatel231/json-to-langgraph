from typing import Sequence
from typing import Annotated, TypeAliasType
from typing import Literal
from typing import Callable
from typing import Any
from pydantic.fields import Field
from pydantic import field_validator
from pydantic import BaseModel
import cel


class GenericState(BaseModel):
    input: dict[str, Any] = Field(default_factory=dict)
    nodes: dict[str, Any] = Field(default_factory=dict)


class CommonExpression(BaseModel):
    expr: str = Field("true", description="CEL expression to evaluate")

    @field_validator("expr")
    def validate_expression(cls, v: str):
        cel.compile(v)
        return v


# these already exist in the graph
class MarkerNode(BaseModel):
    type: Literal["marker"] = "marker"


NodeInput = TypeAliasType("NodeInput", dict[str, "CommonExpression | NodeInput"])

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


class ExecutableNode(BaseModel):
    type: Literal["executable"] = "executable"
    guid: str
    input: NodeInput = Field(default_factory=dict)
    callback: ExecutableNodeFunction = Field(
        exclude=True, default_factory=lambda x: global_node_registry.get(x["guid"])
    )


class Transition(BaseModel):
    destination: str
    condition: CommonExpression = Field(default_factory=lambda: CommonExpression())


class Node(BaseModel):
    id: str
    object: Annotated[ExecutableNode | MarkerNode, Field(discriminator="type")]
    transitions: list[Transition] = Field(default_factory=list)


class WorkflowSpec(BaseModel):
    name: str
    nodes: list[Node]
