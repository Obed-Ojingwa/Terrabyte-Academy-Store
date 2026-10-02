from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.user import User


if TYPE_CHECKING:
    from .user import UserInDB


class BlogPostBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    excerpt: Optional[str] = None
    content: str
    featured_image: Optional[str] = None
    status: str = Field(default='draft')  # draft, published, archived
    is_featured: bool = False
    views_count: int = 0
    published_at: Optional[datetime] = None


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    status: Optional[str] = None  # draft, published, archived
    is_featured: Optional[bool] = None
    views_count: Optional[int] = None
    published_at: Optional[datetime] = None


class BlogPostInDB(BlogPostBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BlogPostWithAuthor(BlogPostInDB):
    author: Optional[UserInDB] = None

    class Config:
        orm_mode = True


class BlogPostWithTags(BlogPostInDB):
    tags: List[str] = []

    class Config:
        orm_mode = True