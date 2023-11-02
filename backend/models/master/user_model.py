from fastapi import status
from pydantic import BaseModel, validator
from typing import Optional
from uuid import UUID


class UserBaseModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    username: str


class UserBaseModelWithID(UserBaseModel):
    user_id: UUID

class UserCreateModel(UserBaseModel):
    password: str
    confirm_password: str

    @validator("confirm_password")
    def password_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('password and confirm_password does not match')
        return v

    class Config:
        schema_extra = {
            "example": {
                "first_name": "bayu",
                "last_name": None,
                "address": None,
                "username": "admin@mail.com",
                "password": "admin",
                "confirm_password": "admin"
            }
        }


class UserResponseModel(BaseModel):
    code: int = status.HTTP_201_CREATED
    payload: UserBaseModelWithID
    

    class Config:
        schema_extra = {
            "example": {
                "user_id": "d0b0c0d0-0d0e-0f0a-0b0a-0d0e0f0a0b0c",
                "username": "admin@mail.com",
                "first_name": "bayu",
                "last_name": None,
                "address": None,
            }
        }
error_response = {
    "422": {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "schema": {
                    "example": {
                        "code": 422,
                        "error": [
                            {
                            "field_name": "confirm_password",
                            "msg": "password and confirm_password does not match"
                            }
                        ]
                    }
                }
            }
        }
    }
}
