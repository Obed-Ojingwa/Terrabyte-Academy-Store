from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime


class SellerBase(BaseSchema):
    store_name: str
    store_description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    is_approved: bool = False
    commission_rate: float = 0.10  # 10% default
    payout_email: Optional[EmailStr] = None
    payout_method: Optional[str] = None
    payout_details: Optional[str] = None  # JSON string for encrypted details


class SellerCreate(SellerBase):
    user_id: str


class SellerUpdate(BaseSchema):
    store_name: Optional[str] = None
    store_description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    is_approved: Optional[bool] = None
    commission_rate: Optional[float] = None
    payout_email: Optional[EmailStr] = None
    payout_method: Optional[str] = None
    payout_details: Optional[str] = None


class SellerInDB(BaseSchema):
    id: str
    user_id: str
    store_name: str
    store_description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    is_approved: bool
    approval_date: Optional[datetime] = None
    approved_by: Optional[str] = None
    commission_rate: float
    payout_email: Optional[EmailStr] = None
    payout_method: Optional[str] = None
    payout_details: Optional[str] = None
    total_sales: float
    total_earnings: float
    rating_average: float
    review_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SellerRegistration(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    store_name: str
    store_description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    payout_email: Optional[EmailStr] = None
    payout_method: Optional[str] = None
    payout_details: Optional[str] = None


class SellerApproval(BaseSchema):
    seller_id: str
    approve: bool
    approved_by: str  # admin user ID
