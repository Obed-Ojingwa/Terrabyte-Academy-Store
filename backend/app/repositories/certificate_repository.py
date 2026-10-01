from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.certificate import Certificate


class CertificateRepository(BaseRepository[Certificate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Certificate, db)

    async def get_by_user_id(self, user_id: str) -> List[Certificate]:
        """Get all certificates for a specific user"""
        result = await self.db.execute(
            select(Certificate)
            .where(Certificate.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_course_id(self, course_id: str) -> List[Certificate]:
        """Get all certificates for a specific course"""
        result = await self.db.execute(
            select(Certificate)
            .where(Certificate.course_id == course_id)
        )
        return result.scalars().all()

    async def get_by_certificate_number(self, certificate_number: str) -> Optional[Certificate]:
        """Get certificate by certificate number"""
        result = await self.db.execute(
            select(Certificate)
            .where(Certificate.certificate_number == certificate_number)
        )
        return result.scalar_one_or_none()

    async def get_valid_certificates(self, skip: int = 0, limit: int = 100) -> List[Certificate]:
        """Get valid certificates"""
        result = await self.db.execute(
            select(Certificate)
            .where(Certificate.is_valid == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()