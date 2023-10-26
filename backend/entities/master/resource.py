from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class ResourceBase(SQLModel):
    name: str = Field(max_length=50, unique=True, nullable=False)
    description: str = Field(max_length=255, nullable=False)
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow().isoformat(), nullable=False)
    created_by: UUID = Field(default_factory=uuid4, nullable=False)
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None

    resource_role: List["ResourceRole"] = Relationship(
        back_populates="resource"
    )


class Resource(ResourceBase, table=True):
    __tablename__ = "mst_resource"
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class ResourceCreate(ResourceBase):
    pass