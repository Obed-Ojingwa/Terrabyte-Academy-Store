from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm = relationship
from app.db.base import BaseModel
import uuid
from .product_tag import product_tag


class Tag(BaseModel):
    """Tag model for products and services"""
    __tablename__ = "tags"

    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    products = relationship("Product", secondary=product_tag, back_populates="tags")
    services = relationship("Service", secondary=service_tag, back_populates="tags")  # Assuming we have ServiceTag later

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"