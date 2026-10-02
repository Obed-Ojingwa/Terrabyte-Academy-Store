from typing import List, Optional
from app.services.base import BaseService
from app.repositories.wishlist_repository import WishlistRepository
from app.schemas.wishlist import WishlistCreate, WishlistUpdate, WishlistInDB
from app.models.wishlist import Wishlist
from fastapi import HTTPException, status

class WishlistService(BaseService[WishlistRepository]):
    def __init__(self, wishlist_repository: WishlistRepository):
        super().__init__(wishlist_repository)
        self.repository = wishlist_repository

    async def get(self, wishlist_id: str) -> WishlistInDB:
        wishlist = await self.repository.get(wishlist_id)
        if not wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )
        return WishlistInDB.from_orm(wishlist)

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[WishlistInDB]:
        wishlists = await self.repository.get_by_user_id(user_id, skip, limit)
        return [WishlistInDB.from_orm(w) for w in wishlists]

    async def get_default_wishlist(self, user_id: str) -> Optional[WishlistInDB]:
        wishlist = await self.repository.get_default_wishlist(user_id)
        if wishlist:
            return WishlistInDB.from_orm(wishlist)
        return None

    async def create(self, user_id: str, wishlist_in: WishlistCreate) -> WishlistInDB:
        # Ensure user owns the wishlist
        wishlist_data = wishlist_in.dict()
        wishlist_data["user_id"] = user_id
        wishlist = Wishlist(**wishlist_data)
        # If this is the first wishlist for the user, make it default
        existing_wishlists = await self.repository.get_by_user_id(user_id, limit=1)
        if not existing_wishlists:
            wishlist.is_default = True
        created_wishlist = await self.repository.create(wishlist_data)
        return WishlistInDB.from_orm(created_wishlist)

    async def update(self, wishlist_id: str, wishlist_in: WishlistUpdate) -> WishlistInDB:
        wishlist = await self.repository.get(wishlist_id)
        if not wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )
        update_data = wishlist_in.dict(exclude_unset=True)
        updated_wishlist = await self.repository.update(wishlist_id, update_data)
        if not updated_wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )
        return WishlistInDB.from_orm(updated_wishlist)

    async def delete(self, wishlist_id: str) -> bool:
        wishlist = await self.repository.get(wishlist_id)
        if not wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )
        return await self.repository.delete(wishlist_id)

    async def set_default(self, user_id: str, wishlist_id: str) -> WishlistInDB:
        # First, unset any existing default wishlist for the user
        existing_default = await self.repository.get_default_wishlist(user_id)
        if existing_default and existing_default.id != wishlist_id:
            await self.repository.update(existing_default.id, {"is_default": False})
        # Set the requested wishlist as default
        wishlist = await self.repository.get(wishlist_id)
        if not wishlist or wishlist.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found or does not belong to user"
            )
        updated_wishlist = await self.repository.update(wishlist_id, {"is_default": True})
        return WishlistInDB.from_orm(updated_wishlist)