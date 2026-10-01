from typing import List, Optional
from app.services.base import BaseService
from app.repositories.order_repository import OrderRepository
from app.repositories.cart_service import CartService
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.payment_repository import PaymentRepository
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.product import Product
from fastapi import HTTPException, status
import uuid
from datetime import datetime


class OrderService(BaseService[OrderRepository]):
    def __init__(
        self,
        order_repository: OrderRepository,
        cart_service: CartService,
        order_item_repository: OrderItemRepository,
        payment_repository: PaymentRepository
    ):
        super().__init__(order_repository)
        self.order_repository = order_repository
        self.cart_service = cart_service
        self.order_item_repository = order_item_repository
        self.payment_repository = payment_repository

    async def create_order_from_cart(
        self,
        cart_id: str,
        user_id: str,
        billing_address_id: str,
        shipping_address_id: str
    ) -> Order:
        """Create an order from a cart"""
        # Get the cart
        cart = await self.cart_service.cart_repository.get(cart_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )

        # Verify cart belongs to user
        if cart.user_id and cart.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to check out this cart"
            )

        # Get cart items
        cart_items = await self.cart_service.get_cart_items(cart_id)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        # Calculate order totals
        cart_total = await self.cart_service.get_cart_total(cart_id)
        subtotal = cart_total["subtotal"]

        # For now, we'll use mock values for tax and shipping
        # In a real implementation, these would be calculated based on location, etc.
        tax_amount = round(subtotal * 0.08, 2)  # 8% tax
        shipping_amount = 0.0 if subtotal >= 50.0 else 9.99  # Free shipping over $50
        discount_amount = 0.0  # No discount for now
        total_amount = round(subtotal + tax_amount + shipping_amount - discount_amount, 2)

        # Generate order number
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

        # Create order
        order_data = {
            "order_number": order_number,
            "user_id": user_id,
            "billing_address_id": billing_address_id,
            "shipping_address_id": shipping_address_id,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "shipping_amount": shipping_amount,
            "discount_amount": discount_amount,
            "total_amount": total_amount,
            "status": "pending"
        }

        order = await self.order_repository.create(order_data)

        # Create order items from cart items
        for cart_item in cart_items:
            # Get product details for pricing
            product = await self.cart_service.product_repository.get(cart_item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product not found: {cart_item.product_id}"
                )

            order_item_data = {
                "order_id": order.id,
                "product_id": cart_item.product_id,
                "quantity": cart_item.quantity,
                "unit_price": product.price,
                "total_price": round(product.price * cart_item.quantity, 2)
            }
            await self.order_item_repository.create(order_item_data)

        # Clear the cart
        await self.cart_service.clear_cart(cart_id)

        return order

    async def get_order_with_items(self, order_id: str) -> dict:
        """Get an order with its items and calculated totals"""
        order = await self.order_repository.get(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        # Get order items
        order_items = await self.order_item_repository.get_by_order_id(order_id)

        # Enhance order items with product details
        enhanced_items = []
        for item in order_items:
            product = await self.cart_service.product_repository.get(item.product_id)
            enhanced_items.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": product.name if product else "Unknown Product",
                "product_sku": product.sku if product else None,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "product_image_url": None  # Would come from product images in a real implementation
            })

        return {
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "subtotal": order.subtotal,
            "tax_amount": order.tax_amount,
            "shipping_amount": order.shipping_amount,
            "discount_amount": order.discount_amount,
            "total_amount": order.total_amount,
            "currency": order.currency,
            "notes": order.notes,
            "placed_at": order.placed_at,
            "shipped_at": order.shipped_at,
            "delivered_at": order.delivered_at,
            "cancelled_at": order.cancelled_at,
            "user_id": order.user_id,
            "billing_address_id": order.billing_address_id,
            "shipping_address_id": order.shipping_address_id,
            "items": enhanced_items,
            "item_count": sum(item.quantity for item in order_items),
            "unique_items": len(order_items)
        }

    async def update_order_status(
        self,
        order_id: str,
        status: str
    ) -> Order:
        """Update order status"""
        order = await self.order_repository.update_order_status(order_id, status)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order

    async def get_user_orders(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Get orders for a user with basic details"""
        orders = await self.order_repository.get_by_user_id(user_id, skip=skip, limit=limit)

        # Return basic order info (not full details with items)
        return [
            {
                "id": order.id,
                "order_number": order.order_number,
                "status": order.status,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
                "placed_at": order.placed_at
            }
            for order in orders
        ]

    async def mock_payment_processing(
        self,
        order_id: str,
        amount: float
    ) -> Payment:
        """Mock payment processing (would integrate with real payment gateway in production)"""
        # Verify order exists
        order = await self.order_repository.get(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        # Verify amount matches order total
        if abs(amount - order.total_amount) > 0.01:  # Allow for small rounding differences
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount does not match order total"
            )

        # Create payment record
        payment_data = {
            "order_id": order_id,
            "amount": amount,
            "currency": "USD",
            "status": "completed",
            "payment_method": "credit_card",
            "transaction_id": f"txn_{uuid.uuid4().hex}",
            "paid_at": datetime.utcnow()
        }

        payment = await self.payment_repository.create(payment_data)

        # Update order status to processing (payment received)
        await self.update_order_status(order_id, "processing")

        return payment