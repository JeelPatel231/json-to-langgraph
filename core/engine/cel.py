
import cel
from pydantic import GetPydanticSchema, RootModel, field_validator
from pydantic_core import SchemaValidator, core_schema


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

    def validate(v, info):
        use_cel = (
            info.context is None
            or info.context.get("cel_mode", True)
        )

        # NORMAL MODE
        if not use_cel:
            validator = SchemaValidator(normal_schema)
            return validator.validate_python(v)

        # CEL MODE
        expr = str(v)

        cel.compile(expr)

        return CommonExpression.model_validate(expr)

    return core_schema.with_info_plain_validator_function(
        validate,
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda v: v.root if isinstance(v, CommonExpression) else v
        ),
    )



CEL = GetPydanticSchema(cel_schema)

