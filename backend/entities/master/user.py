from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from backend.entities.master.user_information import UserInformation
from backend.entities.master.role import Role


class UserBase(SQLModel):
    user_information_id: UUID = Field(default=None, foreign_key="mst_user_information.id")
    role_id: Optional[UUID] = Field(default=None, foreign_key="mst_role.id")
    username: str = Field(max_length=50, unique=True, nullable=False)
    password: str = Field(nullable=False)
    is_active: bool = False
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow().isoformat(), nullable=False)
    created_by: UUID = Field(default_factory=uuid4, nullable=False)
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None

    user_information: Optional[UserInformation] = Relationship(back_populates="user")
    role: Optional[Role] = Relationship(back_populates="role")


class User(UserBase, table=True):
    __tablename__ = "mst_user"
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class UserCreate(UserBase):
    pass