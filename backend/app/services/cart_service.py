from typing import List, Optional
from app.services.base import BaseService
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_item_repository import CartItemRepository
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from sqlalchemy import and_
from fastapi import HTTPException, status


class CartService(BaseService[CartRepository]):
    def __init__(
        self,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
        cart_item_repository: CartItemRepository
    ):
        super().__init__(cart_repository)
        self.cart_repository = cart_repository
        self.product_repository = product_repository
        self.cart_item_repository = cart_item_repository

    async def get_or_create_cart(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Cart:
        """Get existing active cart or create a new one"""
        # Try to get existing cart
        cart = await self.cart_repository.get_active_cart_for_user_or_session(
            user_id=user_id,
            session_id=session_id
        )

        if cart:
            return cart

        # Create new cart if none exists
        return await self.cart_repository.create_cart(
            user_id=user_id,
            session_id=session_id
        )

    async def add_item_to_cart(
        self,
        cart_id: str,
        product_id: str,
        quantity: int = 1
    ) -> CartItem:
        """Add an item to the cart or update quantity if it already exists"""
        # Verify product exists
        product = await self.product_repository.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Verify cart exists
        cart = await self.cart_repository.get(cart_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )

        # Check if item already exists in cart
        existing_item = await self.cart_item_repository.get_by_cart_and_product(
            cart_id=cart_id,
            product_id=product_id
        )

        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            await self.cart_item_repository.db.commit()
            await self.cart_item_repository.db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            cart_item_data = {
                "cart_id": cart_id,
                "product_id": product_id,
                "quantity": quantity
            }
            return await self.cart_item_repository.create(cart_item_data)

    async def remove_item_from_cart(
        self,
        cart_id: str,
        product_id: str
    ) -> bool:
        """Remove an item from the cart"""
        cart_item = await self.cart_item_repository.get_by_cart_and_product(
            cart_id=cart_id,
            product_id=product_id
        )

        if not cart_item:
            return False

        await self.cart_item_repository.delete(cart_item.id)
        return True

    async def update_cart_item_quantity(
        self,
        cart_id: str,
        product_id: str,
        quantity: int
    ) -> Optional[CartItem]:
        """Update the quantity of an item in the cart"""
        if quantity <= 0:
            # If quantity is zero or less, remove the item
            await self.remove_item_from_cart(cart_id, product_id)
            return None

        cart_item = await self.cart_item_repository.get_by_cart_and_product(
            cart_id=cart_id,
            product_id=product_id
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found in cart"
            )

        cart_item.quantity = quantity
        await self.cart_item_repository.db.commit()
        await self.cart_item_repository.db.refresh(cart_item)
        return cart_item

    async def get_cart_items(self, cart_id: str) -> List[CartItem]:
        """Get all items in a cart"""
        return await self.cart_item_repository.get_by_cart_id(cart_id)

    async def clear_cart(self, cart_id: str) -> bool:
        """Remove all items from the cart"""
        items = await self.get_cart_items(cart_id)
        for item in items:
            await self.cart_item_repository.delete(item.id)
        return True

    async def get_cart_total(self, cart_id: str) -> dict:
        """Calculate the total price of items in the cart"""
        items = await self.get_cart_items(cart_id)

        subtotal = 0.0
        item_count = 0

        for item in items:
            product = await self.product_repository.get(item.product_id)
            if product:
                subtotal += product.price * item.quantity
                item_count += item.quantity

        return {
            "subtotal": round(subtotal, 2),
            "item_count": item_count,
            "unique_items": len(items)
        }

    async def check_out_cart(self, cart_id: str) -> Optional[Cart]:
        """Mark the cart as checked out"""
        return await self.cart_repository.mark_as_checked_out(cart_id)