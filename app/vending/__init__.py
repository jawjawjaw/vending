from app.products.repository import ProductRepository
from app.users.repository import UserRepository


class VendingService:
    def __init__(
        self,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository

    def deposit_coins(self, request):
        return {"message": f"Deposited {request.amount} cents"}

    def buy_product(self, request):
        return {"message": f"Bought product with ID {request.product_id}"}

    def reset_vending_machine(self):
        return {"message": "Vending machine reset successfully"}


async def get_vending_service():
    return VendingService()
