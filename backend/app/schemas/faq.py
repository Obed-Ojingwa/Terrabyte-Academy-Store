from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime


class FAQBase(BaseSchema):
    question: str = Field(..., min_length=1, max_length=500)
    answer: str
    is_active: bool = True
    sort_order: int = 0
    views_count: int = 0
    helpful_votes: int = 0


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseSchema):
    question: Optional[str] = Field(None, min_length=1, max_length=500)
    answer: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    views_count: Optional[int] = None
    helpful_votes: Optional[int] = None


class FAQInDB(FAQBase):
    id: str
    category_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FAQWithCategory(FAQInDB):
    category: Optional["CategoryInDB"] = None

    class Config:
        orm_mode = True