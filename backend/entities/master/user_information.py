from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class UserInforamtionBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: Optional[str] = Field(max_length=50, nullable=True)
    email: str = Field(nullable=False)
    address: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow(), nullable=False)
    created_by: UUID = Field(default_factory=uuid4, nullable=False)
    updated_by: Optional[UUID] = None
    updated_at: Optional[datetime] = None


class UserInformation(UserInforamtionBase, table=True):
    __tablename__ = "mst_user_information"
    user: List["User"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="user_information"
    )