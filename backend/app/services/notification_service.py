from typing import List, Optional
from app.services.base import BaseService
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationInDB
from app.models.notification import Notification
from app.services.email_service import EmailService
from fastapi import HTTPException, status

class NotificationService(BaseService[NotificationRepository]):
    def __init__(self, notification_repository: NotificationRepository):
        super().__init__(notification_repository)
        self.repository = notification_repository
        self.email_service = EmailService()

    async def get(self, notification_id: str) -> NotificationInDB:
        notification = await self.repository.get(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return NotificationInDB.from_orm(notification)

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[NotificationInDB]:
        notifications = await self.repository.get_by_user_id(user_id, skip, limit)
        return [NotificationInDB.from_orm(n) for n in notifications]

    async def get_unread_count_by_user_id(self, user_id: str) -> int:
        return await self.repository.get_unread_count_by_user_id(user_id)

    async def create(self, user_id: str, notification_in: NotificationCreate) -> NotificationInDB:
        notification_data = notification_in.dict()
        notification_data["user_id"] = user_id
        notification = Notification(**notification_data)
        created_notification = await self.repository.create(notification_data)

        # Send email if notification type is EMAIL or BOTH
        if notification_in.notification_type in [NotificationType.EMAIL, NotificationType.BOTH]:
            # We need to get the user's email to send the email
            # For simplicity, we'll assume we have a way to get the user's email.
            # In a real implementation, we would fetch the user from the user repository.
            # Since we don't have the user repository injected, we'll skip for now and just log.
            # TODO: Inject user repository to get user email.
            pass

        return NotificationInDB.from_orm(created_notification)

    async def update(self, notification_id: str, notification_in: NotificationUpdate) -> NotificationInDB:
        notification = await self.repository.get(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        update_data = notification_in.dict(exclude_unset=True)
        updated_notification = await self.repository.update(notification_id, update_data)
        if not updated_notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return NotificationInDB.from_orm(updated_notification)

    async def delete(self, notification_id: str) -> bool:
        notification = await self.repository.get(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return await self.repository.delete(notification_id)

    async def mark_as_read(self, notification_id: str) -> NotificationInDB:
        notification = await self.repository.get(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        updated_notification = await self.repository.update(notification_id, {"is_read": True})
        return NotificationInDB.from_orm(updated_notification)

    async def mark_all_as_read(self, user_id: str) -> int:
        # This would require a custom method in the repository to update multiple notifications.
        # For simplicity, we'll implement a basic version that fetches and updates each.
        # In a production system, we would want a more efficient bulk update.
        notifications = await self.repository.get_by_user_id(user_id, limit=1000)  # Assume a reasonable limit
        count = 0
        for notification in notifications:
            if not notification.is_read:
                await self.repository.update(notification.id, {"is_read": True})
                count += 1
        return count