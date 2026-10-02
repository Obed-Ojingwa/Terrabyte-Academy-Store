from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.user import User
from app.models.service import Service


if TYPE_CHECKING:
    from .user import UserInDB
    from .service import ServiceInDB


class ServiceReviewBase(BaseSchema):
    rating: int = Field(..., ge=1, le=5)  # 1-5 stars
    comment: Optional[str] = None
    is_approved: bool = False
    helpful_votes: int = 0


class ServiceReviewCreate(ServiceReviewBase):
    pass


class ServiceReviewUpdate(BaseSchema):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    is_approved: Optional[bool] = None
    helpful_votes: Optional[int] = None


class ServiceReviewInDB(ServiceReviewBase):
    id: str
    service_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ServiceReviewWithUser(ServiceReviewInDB):
    user: Optional[UserInDB] = None

    class Config:
        orm_mode = True


class ServiceReviewWithService(ServiceReviewInDB):
    service: Optional[ServiceInDB] = None

    class Config:
        orm_mode = True