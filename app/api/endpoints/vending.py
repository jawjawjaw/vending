from fastapi import APIRouter, Depends

from app.schemas.requests import BuyProductRequest, DepositRequest
from app.vending import VendingService, get_vending_service

# Create a FastAPI router for vending machine operations
router = APIRouter()

# Define a list of available coin values


# Endpoint for depositing coins
@router.post("/deposit", tags=["Vending Machine"])
async def deposit_coins(
    request: DepositRequest,
    vending_service: VendingService = Depends(get_vending_service),
): 
    resp = vending_service.deposit_coins(request)
    # You can process the deposit operation here
    # For example, update the user's account balance with the deposited coins
    return {"message": f"Deposited {request.amount} cents"}


# Endpoint for buying a product
@router.post("/buy", tags=["Vending Machine"])
async def buy_product(
    request: BuyProductRequest,
    vending_service: VendingService = Depends(get_vending_service),
):
    # You can process the buy operation here
    # For example, deduct the cost of the product from the user's balance
    return {"message": f"Bought product with ID {request.product_id}"}


# Endpoint for resetting the vending machine
@router.post("/reset", tags=["Vending Machine"])
async def reset_vending_machine(
    vending_service: VendingService = Depends(get_vending_service)
):
    # Implement the reset operation here
    # For example, reset all balances and product counts
    return {"message": "Vending machine reset successfully"}
