from pydantic import BaseModel as PydanticBaseModel
from typing import Generic, TypeVar
from datetime import datetime


class BaseSchema(PydanticBaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int