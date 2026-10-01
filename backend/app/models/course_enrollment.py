from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, CHAR, Integer, Numeric, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum
from datetime import datetime


class EnrollmentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class CourseEnrollment(BaseModel):
    """Course enrollment model for student enrollment in courses"""
    __tablename__ = "course_enrollments"

    # Enrollment details
    status = Column(Enum(EnrollmentStatusEnum), default=EnrollmentStatusEnum.PENDING, nullable=False)
    enrollment_date = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    final_grade = Column(Numeric(5, 2), nullable=True)  # Percentage grade
    certificate_issued = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    user_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)
    course_id = Column(CHAR(32), ForeignKey("courses.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="course_enrollments")
    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return f"<CourseEnrollment(id={self.id}, user_id='{self.user_id}', course_id='{self.course_id}', status='{self.status.value}')>"