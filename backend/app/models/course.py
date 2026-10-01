from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, CHAR, Integer, Numeric
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
import enum
from datetime import datetime


class CourseLevelEnum(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(BaseModel):
    """Course model for training academy"""
    __tablename__ = "courses"

    # Course details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)
    level = Column(Enum(CourseLevelEnum), default=CourseLevelEnum.BEGINNER, nullable=False)
    duration_weeks = Column(Integer, nullable=False)  # Duration in weeks
    duration_hours = Column(Integer, nullable=True)   # Total hours
    price = Column(Numeric(10, 2), nullable=False)
    discount_price = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)

    # Timestamps
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    registration_start = Column(DateTime(timezone=True), nullable=True)
    registration_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    category_id = Column(CHAR(32), ForeignKey("training_categories.id"), nullable=False)
    instructor_id = Column(CHAR(32), ForeignKey("users.id"), nullable=True)  # Main instructor

    # Relationships
    category = relationship("TrainingCategory", back_populates="courses")
    instructor = relationship("User", foreign_keys=[instructor_id])
    instructors = relationship("CourseInstructor", back_populates="course", cascade="all, delete-orphan")
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', level='{self.level.value}')>"