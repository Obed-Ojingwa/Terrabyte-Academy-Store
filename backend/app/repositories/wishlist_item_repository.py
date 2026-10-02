from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.wishlist_item import WishlistItem

class WishlistItemRepository(BaseRepository[WishlistItem]):
    def __init__(self, db: AsyncSession):
        super().__init__(WishlistItem, db)

    async def get_by_wishlist_id(self, wishlist_id: str, skip: int = 0, limit: int = 100) -> List[WishlistItem]:
        result = await self.db.execute(
            select(WishlistItem)
            .where(WishlistItem.wishlist_id == wishlist_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_product_and_wishlist(self, product_id: str, wishlist_id: str) -> Optional[WishlistItem]:
        result = await self.db.execute(
            select(WishlistItem)
            .where(
                and_(
                    WishlistItem.product_id == product_id,
                    WishlistItem.wishlist_id == wishlist_id
                )
            )
        )
        return result.scalar_one_or_none()