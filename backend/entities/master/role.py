from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class RoleBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=50, unique=True, nullable=False)
    description: str = Field(max_length=255, nullable=False)
    is_deleted: bool = False
    can_view: bool = False
    can_add: bool = False
    can_edit: bool = False
    can_delete: bool = False
    created_by: UUID = Field(default_factory=uuid4, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow(), nullable=False)
    updated_by: Optional[UUID] = None
    updated_at: Optional[datetime] = None


class Role(RoleBase, table=True):
    __tablename__ = "mst_role"
    # resource_role: List["ResourceRole"] = Relationship(
    #     back_populates="role"
    # )
    # user: Optional["User"] = Relationship(
    #     sa_relationship_kwargs={'uselist': False},
    #     back_populates="role"
    # )