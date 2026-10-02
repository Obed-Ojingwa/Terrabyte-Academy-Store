from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.wishlist_service import WishlistService
from app.services.wishlist_item_service import WishlistItemService
from app.repositories.wishlist_repository import WishlistRepository
from app.repositories.wishlist_item_repository import WishlistItemRepository
from app.schemas.wishlist import WishlistCreate, WishlistUpdate, WishlistInDB
from app.schemas.wishlist_item import WishlistItemCreate, WishlistItemUpdate, WishlistItemInDB
from app.models.user import User
from app.api.v1.deps import get_current_active_user

router = APIRouter()


def get_wishlist_repository(db: AsyncSession = Depends(get_db)) -> WishlistRepository:
    return WishlistRepository(db)


def get_wishlist_item_repository(db: AsyncSession = Depends(get_db)) -> WishlistItemRepository:
    return WishlistItemRepository(db)


def get_wishlist_service(
    wishlist_repo: WishlistRepository = Depends(get_wishlist_repository)
) -> WishlistService:
    return WishlistService(wishlist_repo)


def get_wishlist_item_service(
    wishlist_item_repo: WishlistItemRepository = Depends(get_wishlist_item_repository)
) -> WishlistItemService:
    return WishlistItemService(wishlist_item_repo)


# Wishlist endpoints
@router.post("/", response_model=WishlistInDB, status_code=status.HTTP_201_CREATED)
async def create_wishlist(
    wishlist_in: WishlistCreate,
    wishlist_service: WishlistService = Depends(get_wishlist_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new wishlist for the current user.
    """
    return await wishlist_service.create(current_user.id, wishlist_in)


@router.get("/", response_model=List[WishlistInDB])
async def read_wishlists(
    skip: int = Query(0, description="Number of wishlists to skip"),
    limit: int = Query(100, description="Maximum number of wishlists to return"),
    wishlist_service: WishlistService = Depends(get_wishlist_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve wishlists for the current user.
    """
    return await wishlist_service.get_by_user_id(current_user.id, skip, limit)


@router.get("/{wishlist_id}", response_model=WishlistInDB)
async def read_wishlist(
    wishlist_id: str,
    wishlist_service: WishlistService = Depends(get_wishlist_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific wishlist by ID.
    """
    wishlist = await wishlist_service.get(wishlist_id)
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return wishlist


@router.put("/{wishlist_id}", response_model=WishlistInDB)
async def update_wishlist(
    wishlist_id: str,
    wishlist_in: WishlistUpdate,
    wishlist_service: WishlistService = Depends(get_wishlist_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a wishlist.
    """
    wishlist = await wishlist_service.get(wishlist_id)
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await wishlist_service.update(wishlist_id, wishlist_in)


@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist(
    wishlist_id: str,
    wishlist_service: WishlistService = Depends(get_wishlist_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a wishlist.
    """
    wishlist = await wishlist_service.get(wishlist_id)
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    await wishlist_service.delete(wishlist_id)
    return None


@router.post("/{wishlist_id}/set-default", response_model=WishlistInDB)
async def set_default_wishlist(
    wishlist_id: str,
    wishlist_service: WishlistService = Depends(get_wishlist_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Set a wishlist as the default wishlist for the current user.
    """
    wishlist = await wishlist_service.get(wishlist_id)
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await wishlist_service.set_default(current_user.id, wishlist_id)


# Wishlist item endpoints
@router.post("/{wishlist_id}/items", response_model=WishlistItemInDB, status_code=status.HTTP_201_CREATED)
async def add_item_to_wishlist(
    wishlist_id: str,
    item_in: WishlistItemCreate,
    wishlist_item_service: WishlistItemService = Depends(get_wishlist_item_service),
    wishlist_repository: WishlistRepository = Depends(get_wishlist_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add a product to a wishlist.
    """
    # Verify the wishlist belongs to the current user
    wishlist = await wishlist_repository.get(wishlist_id)
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await wishlist_item_service.create(wishlist_id, item_in)


@router.get("/{wishlist_id}/items", response_model=List[WishlistItemInDB])
async def read_wishlist_items(
    wishlist_id: str,
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(100, description="Maximum number of items to return"),
    wishlist_item_service: WishlistItemService = Depends(get_wishlist_item_service),
    wishlist_repository: WishlistRepository = Depends(get_wishlist_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve items in a wishlist.
    """
    # Verify the wishlist belongs to the current user
    wishlist = await wishlist_repository.get(wishlist_id)
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await wishlist_item_service.get_by_wishlist_id(wishlist_id, skip, limit)


@router.delete("/{wishlist_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_wishlist(
    wishlist_id: str,
    item_id: str,
    wishlist_item_service: WishlistItemService = Depends(get_wishlist_item_service),
    wishlist_repository: WishlistRepository = Depends(get_wishlist_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an item from a wishlist.
    """
    # Verify the wishlist belongs to the current user
    wishlist = await wishlist_repository.get(wishlist_id)
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # Verify the item exists and belongs to the wishlist
    item = await wishlist_item_service.get(item_id)
    if item.wishlist_id != wishlist_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in this wishlist"
        )
    await wishlist_item_service.delete(item_id)
    return None


@router.put("/{wishlist_id}/items/{item_id}", response_model=WishlistItemInDB)
async def update_wishlist_item(
    wishlist_id: str,
    item_id: str,
    item_in: WishlistItemUpdate,
    wishlist_item_service: WishlistItemService = Depends(get_wishlist_item_service),
    wishlist_repository: WishlistRepository = Depends(get_wishlist_repository),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a wishlist item (currently no fields to update, but kept for consistency).
    """
    # Verify the wishlist belongs to the current user
    wishlist = await wishlist_repository.get(wishlist_id)
    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found"
        )
    if wishlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    # Verify the item exists and belongs to the wishlist
    item = await wishlist_item_service.get(item_id)
    if item.wishlist_id != wishlist_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in this wishlist"
        )
    return await wishlist_item_service.update(item_id, item_in)