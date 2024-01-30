from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, validator


class ProductCreate(BaseModel):
    amount_available: int
    cost: int
    product_name: str
    seller_id: UUID

    @validator("cost")
    def validate_cost(cls, v):
        if v <= 0 and v % 5 == 0:
            raise ValueError("cost must be positive and divisible by 5")
        return v


class ProductUpdate(BaseModel):
    amount_available: Optional[int]
    cost: Optional[int]
    product_name: Optional[str]


class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
