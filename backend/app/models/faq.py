from sqlalchemy import Column, String, Text, Boolean, DateTime, CHAR, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.category import Category
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .category import Category


class FAQ(BaseModel):
    """FAQ model for frequently asked questions"""
    __tablename__ = "faqs"

    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    views_count = Column(Integer, default=0, nullable=False)
    helpful_votes = Column(Integer, default=0, nullable=False)

    # Foreign keys
    category_id = Column(CHAR(32), ForeignKey("categories.id"), nullable=True)

    # Relationships
    category = relationship("Category")

    def __repr__(self):
        return f"<FAQ(id={self.id}, question='{self.question[:50]}...')>"