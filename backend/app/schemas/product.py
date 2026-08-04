from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from app.schemas.base import BaseSchema
from datetime import datetime
# from app.models.product import ProductStatus  # We don't have this yet, but we can define later or remove


class ProductBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=10)
    short_description: Optional[str] = Field(None, max_length=500)
    sku: str = Field(..., pattern=r'^[A-Z0-9\-]+$')
    price: float = Field(..., gt=0)
    compare_at_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, gt=0)
    tax_code: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[dict] = None  # {length, width, height}
    stock_quantity: int = Field(..., ge=0)
    track_quantity: bool = True
    allow_backorder: bool = False
    low_stock_threshold: int = Field(5, ge=0)
    is_active: bool = True
    is_featured: bool = False
    requires_shipping: bool = True
    is_digital: bool = False
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)


class ProductCreate(ProductBase):
    category_id: str
    seller_id: str

    @field_validator('compare_at_price')
    def compare_at_price_must_be_greater_than_price(cls, v, values):
        if v is not None and 'price' in values and v <= values['price']:
            raise ValueError('compare_at_price must be greater than price')
        return v


class ProductUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    short_description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    compare_at_price: Optional[float] = Field(None, gt=0)
    cost_price: Optional[float] = Field(None, gt=0)
    tax_code: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[dict] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    track_quantity: Optional[bool] = None
    allow_backorder: Optional[bool] = None
    low_threshold: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    requires_shipping: Optional[bool] = None
    is_digital: Optional[bool] = None
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)


class ProductInDB(ProductBase):
    id: str
    seller_id: str
    category_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductImageBase(BaseSchema):
    url: str = Field(..., max_length=500)
    alt_text: Optional[str] = Field(None, max_length=255)
    is_primary: bool = False
    sort_order: int = 0


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageInDB(ProductImageBase):
    id: str
    product_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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