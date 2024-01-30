from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from app.users.models import AVAILABLE_COINS


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
        json_schema_extra = {
            "example": {"username": "alice", "password": "alice123", "role": "buyer"}
        }


class UserUpdateRequest(BaseRequest):
    password: str

    class Config:
        json_schema_extra = {"example": {"password": "alice123"}}


class ProductCreate(BaseModel):
    amount_available: int
    cost: int
    product_name: str


class ProductUpdate(BaseModel):
    amount_available: Optional[int]
    cost: Optional[int]
    product_name: Optional[str]


class ProductRead(ProductCreate):
    id: UUID


class DepositRequest(BaseModel):
    coin: int

    # add validation to all available coins - make sure amount is 5, 10, 20, 50 and 100 cent coins into their vending machine account (one coin at the time)
    @validator("coin", pre=True)
    def validate_coin(coin):
        if coin in AVAILABLE_COINS:
            return coin
        else:
            raise ValueError("Invalid coin amount")


class BuyProductRequest(BaseModel):
    product_id: UUID
    amount: int

