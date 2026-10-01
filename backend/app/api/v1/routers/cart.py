from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.cart_service import CartService
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_item_repository import CartItemRepository
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.user import User
from app.api.v1.deps import get_current_active_user, get_current_user

router = APIRouter()


def get_cart_repository(db: AsyncSession = Depends(get_db)) -> CartRepository:
    return CartRepository(db)


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


def get_cart_item_repository(db: AsyncSession = Depends(get_db)) -> CartItemRepository:
    return CartItemRepository(db)


def get_cart_service(
    cart_repo: CartRepository = Depends(get_cart_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
    cart_item_repo: CartItemRepository = Depends(get_cart_item_repository)
) -> CartService:
    return CartService(cart_repo, product_repo, cart_item_repo)


@router.post("/", response_model=Cart)
async def create_or_get_cart(
    user_id: Optional[str] = Query(None, description="User ID for authenticated users"),
    session_id: Optional[str] = Query(None, description="Session ID for anonymous users"),
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get existing active cart or create a new one for user or session.
    If user is authenticated, user_id will be ignored and current user's ID will be used.
    """
    # If user is authenticated, use their ID regardless of what's passed in query
    effective_user_id = current_user.id if current_user.is_active else user_id

    cart = await cart_service.get_or_create_cart(
        user_id=effective_user_id,
        session_id=session_id
    )
    return cart


@router.get("/{cart_id}", response_model=Cart)
async def get_cart(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific cart by ID.
    Users can only access their own carts.
    """
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    # Check if the cart belongs to the current user (if it's a user cart)
    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this cart"
        )

    return cart


@router.post("/{cart_id}/items", response_model=CartItem)
async def add_item_to_cart(
    cart_id: str,
    product_id: str,
    quantity: int = Query(1, ge=1, description="Quantity to add"),
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add an item to the cart or update quantity if it already exists.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this cart"
        )

    return await cart_service.add_item_to_cart(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity
    )


@router.put("/{cart_id}/items/{product_id}", response_model=CartItem)
async def update_cart_item_quantity(
    cart_id: str,
    product_id: str,
    quantity: int = Query(..., ge=0, description="Quantity to set (0 to remove)"),
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update the quantity of an item in the cart.
    If quantity is 0, the item will be removed from the cart.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this cart"
        )

    if quantity == 0:
        # Remove item
        success = await cart_service.remove_item_from_cart(cart_id, product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found in cart"
            )
        return None  # Return 204 No Content for successful removal
    else:
        # Update quantity
        cart_item = await cart_service.update_cart_item_quantity(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found in cart"
            )
        return cart_item


@router.delete("/{cart_id}/items/{product_id}")
async def remove_item_from_cart(
    cart_id: str,
    product_id: str,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an item from the cart.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this cart"
        )

    success = await cart_service.remove_item_from_cart(cart_id, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )

    return {"message": "Item removed from cart"}


@router.delete("/{cart_id}/items")
async def clear_cart(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove all items from the cart.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this cart"
        )

    success = await cart_service.clear_cart(cart_id)
    return {"message": "Cart cleared"}


@router.get("/{cart_id}/items", response_model=List[CartItem])
async def get_cart_items(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all items in the cart.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this cart"
        )

    return await cart_service.get_cart_items(cart_id)


@router.get("/{cart_id}/total")
async def get_cart_total(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the total price and item count for the cart.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this cart"
        )

    return await cart_service.get_cart_total(cart_id)


@router.post("/{cart_id}/checkout", response_model=Cart)
async def check_out_cart(
    cart_id: str,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark the cart as checked out.
    """
    # Verify cart belongs to current user
    cart = await cart_service.cart_repository.get(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    if cart.user_id and cart.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this cart"
        )

    checked_out_cart = await cart_service.check_out_cart(cart_id)
    if not checked_out_cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to check out cart"
        )

    return checked_out_cart