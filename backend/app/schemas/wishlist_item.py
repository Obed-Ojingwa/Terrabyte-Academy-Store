from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.product import Product


if TYPE_CHECKING:
    from .product import ProductInDB


class WishlistItemBase(BaseSchema):
    pass


class WishlistItemCreate(WishlistItemBase):
    product_id: str


class WishlistItemUpdate(BaseSchema):
    pass


class WishlistItemInDB(WishlistItemBase):
    id: str
    product_id: str
    wishlist_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class WishlistItemWithProduct(WishlistItemInDB):
    product: Optional[ProductInDB] = None

    class Config:
        orm_mode = True