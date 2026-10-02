from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.user import User


if TYPE_CHECKING:
    from .user import UserInDB


class WishlistBase(BaseSchema):
    name: str = Field(default="My Wishlist", max_length=255)
    description: Optional[str] = None
    is_default: bool = False


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_default: Optional[bool] = None


class WishlistInDB(WishlistBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class WishlistWithUser(WishlistInDB):
    user: Optional[UserInDB] = None

    class Config:
        orm_mode = True