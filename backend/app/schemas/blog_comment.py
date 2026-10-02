from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.user import User


if TYPE_CHECKING:
    from .user import UserInDB
    from .blog_post import BlogPostInDB


class BlogCommentBase(BaseSchema):
    content: str
    is_approved: bool = False
    is_spam: bool = False


class BlogCommentCreate(BlogCommentBase):
    pass


class BlogCommentUpdate(BaseSchema):
    content: Optional[str] = None
    is_approved: Optional[bool] = None
    is_spam: Optional[bool] = None


class BlogCommentInDB(BlogCommentBase):
    id: str
    blog_post_id: str
    author_id: str
    parent_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BlogCommentWithAuthor(BlogCommentInDB):
    author: Optional[UserInDB] = None

    class Config:
        orm_mode = True


class BlogCommentWithReplies(BlogCommentInDB):
    replies: List["BlogCommentWithReplies"] = []

    class Config:
        orm_mode = True