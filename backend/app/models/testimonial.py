from sqlalchemy import Column, String, Text, Boolean, DateTime, CHAR, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from app.models.user import User
from app.models.product import Product
from app.models.service import Service
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User
    from .product import Product
    from .service import Service


class Testimonial(BaseModel):
    """Testimonial model for customer testimonials"""
    __tablename__ = "testimonials"

    name = Column(String(100), nullable=False)  # Person's name
    title = Column(String(200), nullable=True)  # Job title or position
    content = Column(Text, nullable=False)      # The testimonial content
    rating = Column(Integer, nullable=True)     # Optional rating (1-5)
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    views_count = Column(Integer, default=0, nullable=False)

    # Foreign keys (optional - testimonial can be general or about specific product/service/user)
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=True)
    product_id = Column(CHAR(32), ForeignKey("products.id"), nullable=True)
    service_id = Column(CHAR(32), ForeignKey("services.id"), nullable=True)

    # Relationships
    user = relationship("User")
    product = relationship("Product")
    service = relationship("Service")

    def __repr__(self):
        return f"<Testimonial(id={self.id}, name='{self.name}')>"