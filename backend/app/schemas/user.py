from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.base import BaseSchema
from app.models.user import UserRole
from datetime import datetime


class UserBase(BaseSchema):
    email: EmailStr
    is_active: bool = True
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserInDB(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserLogin(BaseSchema):
    email: EmailStr
    password: str


class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"