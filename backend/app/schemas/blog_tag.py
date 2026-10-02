from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime


class BlogTagBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = None  # Hex color code for UI
    usage_count: int = 0


class BlogTagCreate(BlogTagBase):
    pass


class BlogTagUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    color: Optional[str] = None  # Hex color code for UI
    usage_count: Optional[int] = None


class BlogTagInDB(BlogTagBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BlogTagWithBlogPosts(BlogTagInDB):
    blog_posts_count: int = 0

    class Config:
        orm_mode = True