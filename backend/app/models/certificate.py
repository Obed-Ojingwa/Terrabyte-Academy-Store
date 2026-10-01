from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from datetime import datetime


class Certificate(BaseModel):
    """Certificate model for course completion certificates"""
    __tablename__ = "certificates"

    # Certificate details
    certificate_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_valid = Column(Boolean, default=True, nullable=False)

    # Timestamps
    issued_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Optional expiration
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)
    course_id = Column(CHAR(32), ForeignKey("courses.id"), nullable=False)
    enrollment_id = Column(CHAR(32), ForeignKey("course_enrollments.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")
    enrollment = relationship("CourseEnrollment", back_populates="certificate")

    def __repr__(self):
        return f"<Certificate(id={self.id}, certificate_number='{self.certificate_number}', title='{self.title}')>"