from sqlalchemy import Column, String, Text, Boolean, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .category import Category


class Service(BaseModel):
    """Service model for services offered"""
    __tablename__ = "services"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    category_id = Column(CHAR(32), ForeignKey("categories.id"), nullable=False)

    # Relationships
    category = relationship("Category", back_populates="services")

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}')>"