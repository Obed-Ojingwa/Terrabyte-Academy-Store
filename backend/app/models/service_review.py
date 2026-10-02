from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.service import Service
from app.models.user import User


class ServiceReview(BaseModel):
    """Service review model for reviewing services"""
    __tablename__ = "service_reviews"

    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    helpful_votes = Column(Integer, default=0, nullable=False)

    # Foreign keys
    service_id = Column(CHAR(32), ForeignKey("services.id"), nullable=False)
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)

    # Relationships
    service = relationship("Service", back_populates="service_reviews")
    user = relationship("User")

    def __repr__(self):
        return f"<ServiceReview(id={self.id}, service_id='{self.service_id}', user_id='{self.user_id}', rating={self.rating})>"