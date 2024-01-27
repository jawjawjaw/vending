from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    seller = "seller"
    buyer = "buyer"


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserCreateRequest(BaseRequest):
    username: str
    password: str
    role: UserRole

    class Config:
        schema_extra = {
            "example": {"username": "alice", "password": "alice123", "role": "buyer"}
        }


class UserUpdateRequest(BaseRequest):
    password: str

    class Config:
        schema_extra = {"example": {"password": "alice123"}}
