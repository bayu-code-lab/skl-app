from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from fastapi import Depends
from uuid import UUID, uuid4

from backend.core.db import get_session
from backend.models.master.user_model import UserCreateModel, UserResponseModel, UserBaseModelWithID
from backend.entities.master.user import User
from backend.core import security
from backend.entities.master.user_information import UserInformation

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _execute_and_get_first(self, statement):
        result = await self.session.execute(statement)
        return result.scalars().first()
    
    async def get_user_by_username(self, username: str) -> User:
        statement = select(
            User
        ).where(User.username == username)
        return await self._execute_and_get_first(statement)
        


    async def get_user_by_id(self, user_id: str) -> User:
        statement = select(
            User
        ).where(User.id == user_id)
        return await self._execute_and_get_first(statement)

    async def get_list_user(self, skip: int, limit: int) -> User:
        statement = select(User).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        user = result.all()
        return user

    async def create(self, data: UserCreateModel, owner_id: UUID) -> UserResponseModel:
        try:
            user_information = UserInformation(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.username,
                created_by=owner_id
            )
            user = User(
                user_information=user_information,
                username=data.username,
                password=security.get_password_hash(data.password),
                is_active=True,
                is_superuser=False,
                created_by=owner_id
            )
            self.session.add(user)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise Exception('Something went wrong when inserting data to database, please check application logs for more details')
        else:
            await self.session.refresh(user)
            return UserResponseModel(
                payload=UserBaseModelWithID(
                    user_id=user.id,
                    username=user.username,
                    address=user.user_information.address,
                    first_name=user.user_information.first_name,
                    last_name=user.user_information.last_name
                )    
            )
    

    async def edit_user(self, data: UserCreateModel, owner_id: UUID):
        try:
            statement = select(User).where(User.id == id)
            result = await self.session.execute(statement)
            user = result.first()
            user.user_information.first_name = data.first_name
            user.user_information.last_name = data.last_name
            user.user_information.email = data.username
            user.username = data.username
            user.password = security.get_password_hash(data.password)
            user.updated_by = owner_id
            user.updated_at = datetime.utcnow().isoformat()
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise Exception('Something went wrong when inserting data to database, please check application logs for more details')


    async def update_password_by_id(self, id: str, update_by_id: UUID)  -> User:
        statement = select(User).where(User.id == id)
        result = await self.session.execute(statement)
        user = result.first()
        if user:
            user.password = user.password
            user.updated_at = datetime.utcnow().isoformat()
            user.updated_by = update_by_id
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None

    async def update_superuser_by_id(self, id: str, is_superuser: bool, update_by_id: UUID) -> User:
        statement = select(User).where(User.id == id)
        result = await self.session.execute(statement)
        user = result.first()
        if user:
            user.is_superuser = is_superuser
            user.updated_at = datetime.utcnow().isoformat()
            user.updated_by = update_by_id
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None

    async def update_last_login_by_id(self, id: str, update_by_id: UUID) -> User:
        statement = select(User).where(User.id == id)
        result = await self.session.execute(statement)
        user = result.first()
        if user:
            user.last_login = datetime.utcnow().isoformat()
            user.updated_at = datetime.utcnow().isoformat()
            user.updated_by = update_by_id
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None


    async def deactivate_user_by_id(self, id: str, update_by_id: UUID)  -> User:
        statement = select(User).where(User.id == id)
        result = await self.session.execute(statement)
        user = result.first()
        if user:
            user.is_active = False
            user.updated_at = datetime.utcnow().isoformat()
            user.updated_by = update_by_id
            await self.session.commit()
            await self.session.refresh(user)
            return user
        return None

async def get_user_repository(
       session: AsyncSession = Depends(get_session)
) -> UserRepository:
   return UserRepository(session=session)