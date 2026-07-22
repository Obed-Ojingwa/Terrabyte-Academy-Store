from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime


class RoleBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[str] = None  # JSON string of permissions
    is_active: bool = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDB(RoleBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True