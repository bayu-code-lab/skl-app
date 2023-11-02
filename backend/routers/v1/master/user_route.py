from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from backend.business_logic.master.user_logic import UserLogic
from backend.repositories.master.user_repository import UserRepository, get_user_repository
from backend.models.master.user_model import UserCreateModel, UserResponseModel, error_response
from backend.core import security

router = APIRouter(prefix="/api/v1", tags=["Master User"])


@router.post("/user", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED, responses=error_response)
async def create_user(
    user: UserCreateModel,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    current_user: Annotated[str, Depends(security.get_current_active_user)]
    ):
    try:
        return await UserLogic.create_user(data=user, current_user=current_user, repo=repo)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))