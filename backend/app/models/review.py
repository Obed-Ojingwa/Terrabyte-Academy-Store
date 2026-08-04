from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.product import Product
from app.models.user import User


class Review(BaseModel):
    """Review model for product reviews"""
    __tablename__ = "reviews"

    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    helpful_votes = Column(Integer, default=0, nullable=False)

    # Foreign keys
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=False)
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="reviews")
    user = relationship("User")

    def __repr__(self):
        return f"<Review(id={self.id}, product_id='{self.product_id}', user_id='{self.user_id}', rating={self.rating})>"