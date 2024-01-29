from enum import Enum
from typing import Optional

from pydantic import BaseModel


AVAILABLE_COINS = [5, 10, 20, 50, 100]


class UserRole(str, Enum):
    seller = "seller"
    buyer = "buyer"


class UserRead(BaseModel):
    id: int
    username: str
    role: UserRole


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
    amount: int
    # add validation to all available coins - make sure amount is 5, 10, 20, 50 and 100 cent coins into their vending machine account (one coin at the time)

    def validate_amount(amount):
        if amount in AVAILABLE_COINS:
            return amount
        else:
            raise ValueError("Invalid coin amount")
