from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.cart import Cart


class CartRepository(BaseRepository[Cart]):
    def __init__(self, db: AsyncSession):
        super().__init__(Cart, db)

    async def get_by_user_id(self, user_id: str) -> Optional[Cart]:
        """Get active cart for a user"""
        result = await self.db.execute(
            select(Cart)
            .where(
                and_(
                    Cart.user_id == user_id,
                    Cart.is_active == True,
                    Cart.is_checked_out == False
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_by_session_id(self, session_id: str) -> Optional[Cart]:
        """Get cart by session ID (for anonymous users)"""
        result = await self.db.execute(
            select(Cart)
            .where(
                and_(
                    Cart.session_id == session_id,
                    Cart.is_active == True,
                    Cart.is_checked_out == False
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_active_cart_for_user_or_session(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Optional[Cart]:
        """
        Get active cart for user (if authenticated) or session (for anonymous).
        If both are provided, user takes precedence.
        """
        if user_id:
            cart = await self.get_by_user_id(user_id)
            if cart:
                return cart

        if session_id:
            return await self.get_by_session_id(session_id)

        return None

    async def create_cart(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Cart:
        """Create a new cart for user or session"""
        cart_data = {}
        if user_id:
            cart_data["user_id"] = user_id
        if session_id:
            cart_data["session_id"] = session_id

        return await self.create(cart_data)

    async def mark_as_checked_out(self, cart_id: str) -> Optional[Cart]:
        """Mark a cart as checked out"""
        cart = await self.get(cart_id)
        if cart:
            cart.is_checked_out = True
            await self.db.commit()
            await self.db.refresh(cart)
            return cart
        return None