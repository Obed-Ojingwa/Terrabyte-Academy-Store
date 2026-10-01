from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid


class TrainingCategory(BaseModel):
    """Training category model for organizing courses"""
    __tablename__ = "training_categories"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    courses = relationship("Course", back_populates="category")

    def __repr__(self):
        return f"<TrainingCategory(id={self.id}, name='{self.name}')>"