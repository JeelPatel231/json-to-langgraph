
import cel
from pydantic import GetPydanticSchema, RootModel, field_validator
from pydantic_core import core_schema


class CommonExpression(RootModel[str]):
    @field_validator("root")
    @classmethod
    def validate_expression(cls, v: str):
        cel.compile(v)
        return v

    @property
    def expr(self) -> str:
        return self.root
    

def cel_schema(tp, handler):
    normal_schema = handler(tp)

    def validator(v, info):
        use_cel = (
            info.context is None or info.context.get("cel_mode", True)
        )

        # CEL disabled -> behave like normal field
        if not use_cel:
            return v

        # CEL enabled -> validate only THIS field
        cel.compile(v)
        return CommonExpression(v)

    return core_schema.with_info_after_validator_function(
        validator,
        normal_schema,
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda v: str(v)
        ),
    )


CEL = GetPydanticSchema(cel_schema)

