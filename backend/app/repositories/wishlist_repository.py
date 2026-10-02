from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.wishlist import Wishlist

class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db: AsyncSession):
        super().__init__(Wishlist, db)

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        result = await self.db.execute(
            select(Wishlist)
            .where(Wishlist.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_default_wishlist(self, user_id: str) -> Optional[Wishlist]:
        result = await self.db.execute(
            select(Wishlist)
            .where(Wishlist.user_id == user_id, Wishlist.is_default == True)
        )
        return result.scalar_one_or_none()