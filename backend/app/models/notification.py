from sqlalchemy import Column, String, Boolean, DateTime, CHAR, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum


class NotificationType(str, enum.Enum):
    EMAIL = "email"
    IN_APP = "in_app"
    BOTH = "both"


class Notification(BaseModel):
    """Notification model for user notifications"""
    __tablename__ = "notifications"

    # Notification details
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    notification_type = Column(Enum(NotificationType), default=NotificationType.IN_APP, nullable=False)

    # Foreign keys
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id='{self.user_id}', title='{self.title}')>"