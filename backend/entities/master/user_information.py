from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class UserInforamtionBase(SQLModel):
    first_name: str = Field(max_length=50, nullable=False)
    last_name: Optional[str] = Field(max_length=50, nullable=True)
    email: str = Field(nullable=False)
    address: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow().isoformat(), nullable=False)
    created_by: UUID = Field(default_factory=uuid4, nullable=False)
    updated_at: Optional[datetime] = None
    updated_by: Optional[UUID] = None

    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="user_information"
    )


class UserInformation(UserInforamtionBase, table=True):
    __tablename__ = "mst_user_information"
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class UserInformationCreate(UserInforamtionBase):
    pass