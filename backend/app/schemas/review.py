from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.user import User
from app.models.product import Product


if TYPE_CHECKING:
    from .user import UserInDB
    from .product import ProductInDB


class ReviewBase(BaseSchema):
    rating: int = Field(..., ge=1, le=5)  # 1-5 stars
    comment: Optional[str] = None
    is_approved: bool = False
    helpful_votes: int = 0


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseSchema):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    is_approved: Optional[bool] = None
    helpful_votes: Optional[int] = None


class ReviewInDB(ReviewBase):
    id: str
    product_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReviewWithUser(ReviewInDB):
    user: Optional[UserInDB] = None

    class Config:
        orm_mode = True


class ReviewWithProduct(ReviewInDB):
    product: Optional[ProductInDB] = None

    class Config:
        orm_mode = True