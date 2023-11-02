from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID, uuid4
from typing import Optional, Annotated
from fastapi import Depends

from backend.models.master.user_model import UserCreateModel, UserResponseModel
from backend.repositories.master.user_repository import UserRepository



class UserLogic:
    @classmethod
    async def create_user(
        cls, 
        data: UserCreateModel,
        repo: UserRepository,
        current_user: Optional[UUID] = None,
    ) -> UserResponseModel:
        if await repo.get_user_by_username(data.username):
            raise Exception("Username already exist")
        if current_user is None:
            current_user = uuid4()
        return await repo.create(data, current_user)