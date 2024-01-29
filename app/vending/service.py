from app.products.repository import ProductRepository
from app.users.repository import UserRepository
from app.vending.models import BuyProductRequest, DepositRequest


class VendingService:
    def __init__(
        self, user_repository: UserRepository, product_repository: ProductRepository
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def deposit_coins(self, request: DepositRequest):
        resp = await self.user_repository.deposit_coins(request)
        return resp

    async def buy_product(self, request: BuyProductRequest):
        resp = await self.product_repository.buy_product(request)
        return resp

    async def reset_vending_machine(self, user_id: UUID):
        resp = await self.user_repository.reset_deposit(user_id)
        
        return resp
