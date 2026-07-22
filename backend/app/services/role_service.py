from app.services.base import BaseService
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate, RoleInDB
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.role import Role


class RoleService(BaseService[RoleRepository]):
    def __init__(self, role_repository: RoleRepository):
        super().__init__(role_repository)

    async def get_role_by_name(self, name: str) -> Role:
        role = await self.repository.get_by_name(name)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with name '{name}' not found"
            )
        return role

    async def create_role(self, role_in: RoleCreate) -> Role:
        existing_role = await self.repository.get_by_name(role_in.name)
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this name already exists"
            )
        role = await self.repository.create(role_in.dict())
        return role

    async def update_role(self, role_id: str, role_in: RoleUpdate) -> Role:
        role = await self.repository.get(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        update_data = role_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(role, field, value)
        await self.repository.update(role_id, update_data)
        return await self.repository.get(role_id)

    async def delete_role(self, role_id: str) -> None:
        role = await self.repository.get(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        await self.repository.delete(role_id)