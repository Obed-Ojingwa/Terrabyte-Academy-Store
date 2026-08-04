from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime


class TagBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    pass


class TagInDB(TagBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True