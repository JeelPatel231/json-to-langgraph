from typing import Annotated
from core.engine.nodes.executable.print import PrintNode
from core.engine.nodes.executable.take_input import TakeInputNode
from core.engine.nodes.marker import EndNode, StartNode
from pydantic.fields import Field
from pydantic import BaseModel


MarkerNode = Annotated[StartNode | EndNode, Field(discriminator="id")]

ExecutableNode = Annotated[TakeInputNode | PrintNode, Field(discriminator="name")]

Node = MarkerNode | ExecutableNode


class WorkflowSpec(BaseModel):
    name: str
    nodes: list[Node]

