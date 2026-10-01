from typing import List, Optional
from app.services.base import BaseService
from app.repositories.certificate_repository import CertificateRepository
from app.models.certificate import Certificate
from fastapi import HTTPException, status
import datetime
import uuid


class CertificateService(BaseService[CertificateRepository]):
    def __init__(self, certificate_repository: CertificateRepository):
        super().__init__(certificate_repository)
        self.certificate_repository = certificate_repository

    async def get_certificate(self, certificate_id: str) -> Certificate:
        """Get certificate by ID"""
        certificate = await self.certificate_repository.get(certificate_id)
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        return certificate

    async def get_certificate_by_number(self, certificate_number: str) -> Certificate:
        """Get certificate by certificate number"""
        certificate = await self.certificate_repository.get_by_certificate_number(certificate_number)
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        return certificate

    async def get_certificates_by_user_id(self, user_id: str) -> List[Certificate]:
        """Get all certificates for a specific user"""
        return await self.certificate_repository.get_by_user_id(user_id)

    async def get_certificates_by_course_id(self, course_id: str) -> List[Certificate]:
        """Get all certificates for a specific course"""
        return await self.certificate_repository.get_by_course_id(course_id)

    async def get_valid_certificates(self, skip: int = 0, limit: int = 100) -> List[Certificate]:
        """Get valid certificates"""
        return await self.certificate_repository.get_valid_certificates(skip=skip, limit=limit)

    async def create_certificate(
        self,
        user_id: str,
        course_id: str,
        title: str,
        description: Optional[str] = None,
        enrollment_id: Optional[str] = None
    ) -> Certificate:
        """Create a new certificate"""
        # Check if user exists
        from app.models.user import User
        from app.repositories.user_repository import UserRepository
        # We would need to inject the user repository or use a service
        # For simplicity, we'll skip this check in this implementation
        # In a real implementation, you'd validate that the user exists

        # Check if course exists
        from app.repositories.course_repository import CourseRepository
        from app.db.session import get_db
        # We would need to inject the course repository or use a service
        # For simplicity, we'll skip this check in this implementation
        # In a real implementation, you'd validate that the course exists

        # Check if enrollment exists (if provided)
        if enrollment_id:
            from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
            from app.db.session import get_db
            # We would need to inject the enrollment repository or use a service
            # For simplicity, we'll skip this check in this implementation
            # In a real implementation, you'd validate that the enrollment exists

        # Generate certificate number
        certificate_number = f"CERT-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

        certificate_data = {
            "user_id": user_id,
            "course_id": course_id,
            "certificate_number": certificate_number,
            "title": title,
            "description": description,
            "enrollment_id": enrollment_id
        }
        # Remove None values
        certificate_data = {k: v for k, v in certificate_data.items() if v is not None}

        return await self.certificate_repository.create(certificate_data)

    async def update_certificate(
        self,
        certificate_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_valid: Optional[bool] = None
    ) -> Certificate:
        """Update certificate"""
        certificate = await self.certificate_repository.get(certificate_id)
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if is_valid is not None:
            update_data["is_valid"] = is_valid

        if not update_data:
            return certificate

        return await self.certificate_repository.update(certificate_id, update_data)

    async def delete_certificate(self, certificate_id: str) -> bool:
        """Delete certificate"""
        return await self.certificate_repository.delete(certificate_id)