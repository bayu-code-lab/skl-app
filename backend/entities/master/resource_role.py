from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from backend.entities.master.role import Role
from backend.entities.master.resource import Resource


class ResourceRoleBase(SQLModel):
    rele_id: Optional[UUID] = Field(default=None, foreign_key="mst_role.id")
    resource_id: Optional[UUID] = Field(default=None, foreign_key="mst_resource.id")
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow().isoformat(), nullable=False)
    created_by: UUID = Field(default_factory=uuid4, nullable=False)
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None
    role: Optional[Role] = Relationship(back_populates="resource_role")
    resource: Optional[Resource] = Relationship(back_populates="resource_role")

class ResourceRole(ResourceRoleBase, table=True):
    __tablename__ = "mst_resource_role"
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class ResourceRoleCreate(ResourceRoleBase):
    pass