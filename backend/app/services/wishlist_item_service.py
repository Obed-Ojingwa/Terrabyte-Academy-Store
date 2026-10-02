from typing import List, Optional
from app.services.base import BaseService
from app.repositories.wishlist_item_repository import WishlistItemRepository
from app.schemas.wishlist_item import WishlistItemCreate, WishlistItemUpdate, WishlistItemInDB
from app.models.wishlist_item import WishlistItem
from fastapi import HTTPException, status

class WishlistItemService(BaseService[WishlistItemRepository]):
    def __init__(self, wishlist_item_repository: WishlistItemRepository):
        super().__init__(wishlist_item_repository)
        self.repository = wishlist_item_repository

    async def get(self, item_id: str) -> WishlistItemInDB:
        item = await self.repository.get(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist item not found"
            )
        return WishlistItemInDB.from_orm(item)

    async def get_by_wishlist_id(self, wishlist_id: str, skip: int = 0, limit: int = 100) -> List[WishlistItemInDB]:
        items = await self.repository.get_by_wishlist_id(wishlist_id, skip, limit)
        return [WishlistItemInDB.from_orm(item) for item in items]

    async def get_by_product_and_wishlist(self, product_id: str, wishlist_id: str) -> Optional[WishlistItemInDB]:
        item = await self.repository.get_by_product_and_wishlist(product_id, wishlist_id)
        if item:
            return WishlistItemInDB.from_orm(item)
        return None

    async def create(self, wishlist_id: str, item_in: WishlistItemCreate) -> WishlistItemInDB:
        # Check if item already in wishlist
        existing = await self.repository.get_by_product_and_wishlist(item_in.product_id, wishlist_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already in wishlist"
            )
        item_data = item_in.dict()
        item_data["wishlist_id"] = wishlist_id
        created_item = await self.repository.create(item_data)
        return WishlistItemInDB.from_orm(created_item)

    async def update(self, item_id: str, item_in: WishlistItemUpdate) -> WishlistItemInDB:
        item = await self.repository.get(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist item not found"
            )
        update_data = item_in.dict(exclude_unset=True)
        updated_item = await self.repository.update(item_id, update_data)
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist item not found"
            )
        return WishlistItemInDB.from_orm(updated_item)

    async def delete(self, item_id: str) -> bool:
        item = await self.repository.get(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist item not found"
            )
        return await self.repository.delete(item_id)