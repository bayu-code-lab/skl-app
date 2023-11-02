from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from backend.core.db import get_session
from backend.core.config import settings
from backend.core import security
from backend.repositories.master.user_repository import UserRepository, get_user_repository

router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.post("/access-token")
async def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    ):
    user = await security.authenticate_user(form_data.username, form_data.password, repo)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
            data={"sub": jsonable_encoder(user.id), "username": user.username}, 
            expires_delta=access_token_expires
        )
    refresh_token = security.create_refresh_token(
            data={"sub": jsonable_encoder(user.id), "username": user.username}, 
            expires_delta=refresh_token_expires
        )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh-token")
async def refresh_token(
    session: AsyncSession = Depends(get_session), 
    refresh_token: Annotated[str | None, Header(convert_underscores=False)] = None
    ):
    user = await security.validate_refresh_token(session, refresh_token)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
            data={"sub": jsonable_encoder(user.user_id), "username": user.username}, 
            expires_delta=access_token_expires
        )
    refresh_token = security.create_refresh_token(
            data={"sub": jsonable_encoder(user.user_id), "username": user.username}, 
            expires_delta=refresh_token_expires
        )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}