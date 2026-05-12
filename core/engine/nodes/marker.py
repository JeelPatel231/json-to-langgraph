from typing import Literal
from core.engine.types import BaseNodeModel


class BaseMarkerNode(BaseNodeModel):
    type: Literal["marker"] = "marker"


class StartNode(BaseMarkerNode):
    id: Literal["__start__"] = "__start__"


class EndNode(BaseMarkerNode):
    id: Literal["__end__"] = "__end__"