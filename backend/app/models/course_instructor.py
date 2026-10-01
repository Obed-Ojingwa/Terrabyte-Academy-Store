from sqlalchemy import Column, DateTime, ForeignKey, CHAR, String, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid
from datetime import datetime


class CourseInstructor(BaseModel):
    """Course instructor model for assigning instructors to courses"""
    __tablename__ = "course_instructors"

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Foreign keys
    course_id = Column(CHAR(32), ForeignKey("courses.id"), nullable=False)
    instructor_id = Column(CHAR(32), ForeignKey("users.id"), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="instructors")
    instructor = relationship("User", back_populates="course_assignments")

    def __repr__(self):
        return f"<CourseInstructor(id={self.id}, course_id='{self.course_id}', instructor_id='{self.instructor_id}')>"