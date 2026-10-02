from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.notification_service import NotificationService
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationInDB
from app.models.user import User
from app.api.v1.deps import get_current_active_user

router = APIRouter()


def get_notification_repository(db: AsyncSession = Depends(get_db)) -> NotificationRepository:
    return NotificationRepository(db)


def get_notification_service(
    notification_repo: NotificationRepository = Depends(get_notification_repository)
) -> NotificationService:
    return NotificationService(notification_repo)


# Notification endpoints
@router.post("/", response_model=NotificationInDB, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_in: NotificationCreate,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new notification for the current user.
    """
    return await notification_service.create(current_user.id, notification_in)


@router.get("/", response_model=List[NotificationInDB])
async def read_notifications(
    skip: int = Query(0, description="Number of notifications to skip"),
    limit: int = Query(100, description="Maximum number of notifications to return"),
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve notifications for the current user.
    """
    return await notification_service.get_by_user_id(current_user.id, skip, limit)


@router.get("/unread-count")
async def get_unread_notification_count(
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the count of unread notifications for the current user.
    """
    count = await notification_service.get_unread_count_by_user_id(current_user.id)
    return {"unread_count": count}


@router.get("/{notification_id}", response_model=NotificationInDB)
async def read_notification(
    notification_id: str,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific notification by ID.
    """
    notification = await notification_service.get(notification_id)
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return notification


@router.put("/{notification_id}", response_model=NotificationInDB)
async def update_notification(
    notification_id: str,
    notification_in: NotificationUpdate,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a notification.
    """
    notification = await notification_service.get(notification_id)
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await notification_service.update(notification_id, notification_in)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: str,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a notification.
    """
    notification = await notification_service.get(notification_id)
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    await notification_service.delete(notification_id)
    return None


@router.post("/{notification_id}/mark-as-read", response_model=NotificationInDB)
async def mark_notification_as_read(
    notification_id: str,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark a notification as read.
    """
    notification = await notification_service.get(notification_id)
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return await notification_service.mark_as_read(notification_id)


@router.post("/mark-all-as-read")
async def mark_all_notifications_as_read(
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark all notifications as read for the current user.
    """
    count = await notification_service.mark_all_as_read(current_user.id)
    return {"marked_as_read": count}