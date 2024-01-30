from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.vending.models import Change


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    deposit: int


class BuyProductSummary(BaseModel):
    total_spent: int
    product_name: str
    change: Change
