from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.repositories.cart_service import CartService
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.payment_repository import PaymentRepository
from app.models.order import Order
from app.models.user import User
import uuid

router = APIRouter()


def get_order_repository(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


def get_order_item_repository(db: AsyncSession = Depends(get_db)) -> OrderItemRepository:
    return OrderItemRepository(db)


def get_payment_repository(db: AsyncSession = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db)


def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    cart_service: CartService = Depends(),
    order_item_repo: OrderItemRepository = Depends(get_order_item_repository),
    payment_repo: PaymentRepository = Depends(get_payment_repository)
) -> OrderService:
    return OrderService(order_repo, cart_service, order_item_repo, payment_repo)


@router.post("/", response_model=dict)
async def create_order(
    cart_id: str,
    billing_address_id: str,
    shipping_address_id: str,
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create an order from a cart.
    """
    order_dict = await order_service.create_order_from_cart(
        cart_id=cart_id,
        user_id=current_user.id,
        billing_address_id=billing_address_id,
        shipping_address_id=shipping_address_id
    )
    return order_dict


@router.get("/", response_model=List[dict])
async def get_user_orders(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get orders for the current user.
    """
    return await order_service.get_user_orders(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )


@router.get("/{order_id}", response_model=dict)
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific order by ID with details.
    Users can only access their own orders.
    """
    order_dict = await order_service.get_order_with_items(order_id)

    # Verify the order belongs to the current user
    if order_dict["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )

    return order_dict


@router.put("/{order_id}/status", response_model=dict)
async def update_order_status(
    order_id: str,
    status: str,
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update order status.
    """
    # For now, only allow certain status transitions
    # In a real implementation, you'd have more sophisticated logic
    allowed_statuses = ["processing", "shipped", "delivered", "cancelled"]
    if status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(allowed_statuses)}"
        )

    order = await order_service.update_order_status(order_id, status)

    # Verify the order belongs to the current user
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this order"
        )

    return {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "updated_at": order.updated_at
    }


@router.post("/{order_id}/payment", response_model=dict)
async def process_payment(
    order_id: str,
    amount: float,
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Process payment for an order (mock payment processing).
    """
    # Verify the order belongs to the current user
    order = await order_service.order_repository.get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to process payment for this order"
        )

    payment = await order_service.mock_payment_processing(order_id, amount)

    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": payment.status,
        "transaction_id": payment.transaction_id,
        "paid_at": order.paid_at
    }


@router.get("/{order_id}/tracking")
async def get_order_tracking(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get shipping/tracking information for an order.
    """
    # Verify the order belongs to the current user
    order = await order_service.order_repository.get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access tracking for this order"
        )

    # Get shipping information
    # In a real implementation, we'd use the shipping repository
    # For now, we'll return mock data
    return {
        "order_id": order_id,
        "tracking_number": f"TRK-{uuid.uuid4().hex[:10].upper()}",
        "tracking_url": f"https://example.com/track/{uuid.uuid4().hex[:10]}",
        "service": "Standard Shipping",
        "status": "in_transit",
        "estimated_delivery": "2023-12-25"
    }