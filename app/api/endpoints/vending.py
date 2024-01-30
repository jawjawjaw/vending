from fastapi import APIRouter, Depends, HTTPException
from app.api.auth import get_current_user
from app.db.sql.models import User
from app.errors import (
    InvalidRoleError,
    NotEnoughChangeError,
    NotEnoughMoneyError,
    NotEnoughProductError,
    ProductNotFoundError,
    UserNotFoundError,
)

from app.schemas.requests import BuyProductRequest, DepositRequest
from app.users.models import UserDeposit, UserRead, UserReadFull
from app.vending.service import VendingService, get_vending_service

from app.vending.models import BuyProduct

# Create a FastAPI router for vending machine operations
router = APIRouter()

# Define a list of available coin values


@router.post(
    "/deposit",
)
async def deposit_coins(
    request: DepositRequest,
    current_user: UserRead = Depends(get_current_user),
    vending_service: VendingService = Depends(get_vending_service),
):
    req = UserDeposit(
        coin=request.coin,
        user_id=current_user.id,
    )
    try:
        resp = await vending_service.deposit_coins(req)
    except InvalidRoleError as e:
        return HTTPException(status_code=400, detail=str(e))

    return resp


@router.post(
    "/buy",
)
async def buy_product(
    request: BuyProductRequest,
    current_user: UserRead = Depends(get_current_user),
    vending_service: VendingService = Depends(get_vending_service),
):
    try:
        req = BuyProduct(
            product_id=request.product_id,
            amount=request.amount,
            user_id=current_user.id,
        )
        res = await vending_service.buy_product(req)
    except (
        UserNotFoundError,
        ProductNotFoundError,
        NotEnoughProductError,
        NotEnoughMoneyError,
        NotEnoughChangeError
    ) as e:
        return HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")

    return res


@router.post(
    "/reset",
)
async def reset_user_deposit(
    vending_service: VendingService = Depends(get_vending_service),
    current_user: UserRead = Depends(get_current_user),
):
    try:
        await vending_service.reset_user_deposit(current_user.id)
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))

    return {"message": "success"}
