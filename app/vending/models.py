from click import UUID
from app.users.models import AVAILABLE_COINS


class DepositRequest(BaseModel):
    amount: int

    # add validation to all available coins - make sure amount is 5, 10, 20, 50 and 100 cent coins into their vending machine account (one coin at the time)

    def validate_amount(amount):
        if amount in AVAILABLE_COINS:
            return amount
        else:
            raise ValueError("Invalid coin amount")


class BuyProductRequest(BaseModel):
    product_id: UUID
    amount: int
