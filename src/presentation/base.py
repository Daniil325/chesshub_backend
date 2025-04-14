from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict, field_validator
from humps import camelize


APIModelConfig = ConfigDict(
    alias_generator=camelize,
    str_strip_whitespace=True,
    populate_by_name=True,
    extra="ignore",
)

ApiInputModelConfig = ConfigDict(
    alias_generator=camelize, str_strip_whitespace=True, extra="ignore"
)


class SuccessResponse(BaseModel):
    model_config = APIModelConfig
    success: bool = True


class ErrorResponse(BaseModel):
    model_config = APIModelConfig
    success: bool = False
    error: str
    detail: str


class ModelResponseItem(BaseModel):
    model_config = APIModelConfig
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def convert_id(cls, value):
        if value:
            return str(value)


Model = TypeVar("Model", bound=ModelResponseItem)


class ModelResponse(SuccessResponse, Generic[Model]):
    item: Model


Item = TypeVar("Item", bound=BaseModel)


class ListResponse(SuccessResponse, Generic[Item]):
    items: list[Item]
