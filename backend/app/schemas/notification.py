from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime
from app.models.notification import NotificationType


class NotificationBase(BaseSchema):
    title: str = Field(max_length=255)
    message: str
    is_read: bool = False
    notification_type: NotificationType = NotificationType.IN_APP


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = None
    is_read: Optional[bool] = None
    notification_type: Optional[NotificationType] = None


class NotificationInDB(NotificationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationWithUser(NotificationInDB):
    # We'll omit the user for now to avoid circular references
    pass

    class Config:
        orm_mode = True