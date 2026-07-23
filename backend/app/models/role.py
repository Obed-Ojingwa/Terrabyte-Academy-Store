from sqlalchemy import Column, String, Text, Boolean, DateTime, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Role(BaseModel):
    """Role model for RBAC"""
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    # We'll store permissions as a JSON string or a list of strings
    # For simplicity, we'll store as a string that can be parsed as a list
    # In a real application, you might want to use a separate table for permissions
    permissions = Column(Text, nullable=True)  # JSON string of permissions
    is_active = Column(Boolean, default=True, nullable=False)

    # One-to-many relationship with User
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"