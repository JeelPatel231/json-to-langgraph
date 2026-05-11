from typing import Callable, Any, TypeVar
from pydantic import BaseModel
import inspect
from functools import wraps
from core.types import GenericState

PydanticModelType = TypeVar("PydanticModelType", bound=BaseModel)

def pydantic_args(func: Callable[[PydanticModelType, GenericState], Any]):
  type_sig = inspect.signature(func)
  model = next(iter(type_sig.parameters.values())).annotation
  assert issubclass(model, BaseModel), "First type parameter must be a Pydantic model"

  @wraps(func)
  def __inner(args: dict[str, Any], state: GenericState):
      validated = model.model_validate(args)
      return func(validated, state) # type: ignore
  
  return __inner