from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from backend.core.config import settings
from fastapi import Depends, HTTPException

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User database
users_db = {
    "user1": {
        "username": "user1",
        "full_name": "User One",
        "email": "user1@example.com",
        "hashed_password": "$2b$12$j48xwo7eRhq0FudyeqSKIebp4p2xycL6b8r.DyaoJdMQkPkFXR1Ue",
        "disabled": False,
    },
    "user2": {
        "username": "user2",
        "full_name": "User Two",
        "email": "user2@example.com",
        "hashed_password": "$2b$12$j48xwo7eRhq0FudyeqSKIebp4p2xycL6b8r.DyaoJdMQkPkFXR1Ue",
        "disabled": True,
    },
}

# OAuth2 settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get user by username
def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return user_dict

# Authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# Create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = get_user(username=token_data["username"])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user