from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm = relationship
from app.db.base import BaseModel
import uuid
from app.models.user_role import user_role


class User(BaseModel):
    """User model"""
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String(255), nullable=True)
    email_verification_expires = Column(DateTime(timezone=True), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    # Note: Role is now managed via the many-to-many relationship 'roles'
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    seller = relationship("Seller", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # Many-to-many relationship with Role
    roles = relationship("Role", secondary=user_role, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"