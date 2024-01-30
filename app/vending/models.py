from typing import Dict
from uuid import UUID

from pydantic import BaseModel, validator, RootModel
from app.users.models import AVAILABLE_COINS


class Deposit(BaseModel):
    coin: int
    user_id: UUID

    # add validation to all available coins - make sure amount is 5, 10, 20, 50 and 100 cent coins into their vending machine account (one coin at the time)
    @validator("coin", pre=True)
    def validate_coin(coin):
        if coin in AVAILABLE_COINS:
            return coin
        else:
            raise ValueError("Invalid coin amount")


class BuyProduct(BaseModel):
    product_id: UUID
    amount: int
    user_id: UUID


class Change(RootModel):
    root: dict[int, int] = {c: 0 for c in AVAILABLE_COINS}

    @validator("root",)
    def validate(cls, v: dict[int, int]):
        print(v)
        if sorted(AVAILABLE_COINS) == sorted(v.keys()):
            return v
        else:
            raise ValueError("Invalid change amount")


class BuyProductSummary(BaseModel):
    #  API should return total they’ve spent, the product they’ve purchased and their change if there’s any (in an array of 5, 10, 20, 50 and 100 cent coins)
    # - return the product
    # - return the total spent
    # - return the product name
    # - return the change

    total_spent: int
    product_name: str
    change: Change
