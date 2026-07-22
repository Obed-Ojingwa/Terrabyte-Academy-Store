from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.base import BaseSchema
from datetime import datetime


class CategoryBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    slug: str = Field(..., min_length=1, max_length=200)
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    icon_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class CategoryInDB(CategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CategoryWithChildren(CategoryInDB):
    children: List["CategoryWithChildren"] = []

    class Config:
        orm_mode = True