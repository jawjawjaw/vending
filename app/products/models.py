from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):

    amount_available: int
    cost: int
    product_name: str
    seller_id: UUID


class ProductUpdate(BaseModel):
    amount_available: Optional[int]
    cost: Optional[int]
    product_name: Optional[str]


class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID



