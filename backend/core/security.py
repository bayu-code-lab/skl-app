from jose import JWTError, jwt
from typing import Annotated, Any
from pydantic import ValidationError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status

from backend.core.config import settings
from backend.repositories.master.user_repository import UserRepository, get_user_repository
from backend.entities.master.user import User



# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 settings
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/access-token",
)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get password hash
def get_password_hash(password):
    return pwd_context.hash(password)

# Get user by username
async def get_user_id(
        user_id: str,
        repo: Any
    ) -> dict:
    user = await repo.get_user_by_id(user_id)
    if user:
        return user
    return None

# Authenticate user
async def authenticate_user(
        username: str, 
        password: str, 
        repo: UserRepository
    ) -> User:
    user = await repo.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# Create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def validate_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[str, Depends(validate_access_token)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def validate_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        if token_type != "refresh":
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    user = repo.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user