from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, validator


AVAILABLE_COINS = [5, 10, 20, 50, 100]

class UserRole(str, Enum):
    seller = "seller"
    buyer = "buyer"


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    role: UserRole


class UserReadFull(UserRead):
    deposit: int


class BuyerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    role: UserRole
    deposit: int

class UserUpdate(BaseModel):
    password: Optional[str]
    role: Optional[UserRole]
    deposit: Optional[int]


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole
    deposit: int = 0


class UserDeposit(BaseModel):
    coin: int
    user_id: UUID
    # add validation to all available coins - make sure amount is 5, 10, 20, 50 and 100 cent coins into their vending machine account (one coin at the time)

    @validator("coin", pre=True)
    def validate_coin(coin):
        if coin in AVAILABLE_COINS:
            return coin
        else:
            raise ValueError("Invalid coin amount")
