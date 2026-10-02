from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.user import User
from app.models.product import Product
from app.models.service import Service


if TYPE_CHECKING:
    from .user import UserInDB
    from .product import ProductInDB
    from .service import ServiceInDB


class TestimonialBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=200)
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_active: bool = True
    is_featured: bool = False
    views_count: int = 0


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    views_count: Optional[int] = None


class TestimonialInDB(TestimonialBase):
    id: str
    user_id: Optional[str] = None
    product_id: Optional[str] = None
    service_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TestimonialWithUser(TestimonialInDB):
    user: Optional[UserInDB] = None

    class Config:
        orm_mode = True


class TestimonialWithProduct(TestimonialInDB):
    product: Optional[ProductInDB] = None

    class Config:
        orm_mode = True


class TestimonialWithService(TestimonialInDB):
    service: Optional[ServiceInDB] = None

    class Config:
        orm_mode = True