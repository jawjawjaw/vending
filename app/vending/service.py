import logging
from uuid import UUID

from fastapi import Depends
from app.products.repository import ProductRepository, get_product_repository
from app.users.models import BuyerRead
from app.users.repository import UserRepository, get_user_repository
from app.vending import machine
from app.errors import (
    InvalidRoleError,
    NotEnoughChangeError,
    NotEnoughMoneyError,
    NotEnoughProductError,
    ProductNotFoundError,
    UserNotFoundError,
)
from app.vending.models import BuyProduct, BuyProductSummary, Deposit


from app.log import log


class VendingService:
    def __init__(
        self,
        user_repository: UserRepository,
        product_repository: ProductRepository,
        vending_machine: machine.VendingMachine,
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.vending_machine = vending_machine

    async def deposit_coins(self, request: Deposit) -> BuyerRead:
        current_user = await self.user_repository.get_for_update(request.user_id)
        if current_user.role == "seller":
            raise InvalidRoleError()
        resp = await self.user_repository.deposit_coins(request)

        log.info(f"Deposited {request.coin} for user {request.user_id}")
        current = await self.vending_machine.add_coin(request.coin)


        log.info(f"Current coins in vending machine: {current}")

        return resp

    async def buy_product(self, request: BuyProduct):
        # - check if there's enough money deposited
        # - check if there's enough product available
        # - check if there's enough change available
        # - update the product amount available
        # - update the user deposit
        # - return the product
        # - return the total spent
        # - return the product name
        # - return the change
        # check if there's enough money deposited

        log.info(f"Buying product {request.product_id} for user {request.user_id}")
        buyer = await self.user_repository.get_for_update(request.user_id)
        if not buyer:
            log.info(f"User {request.user_id} not found")
            raise UserNotFoundError()
        if buyer.role == "seller":
            raise InvalidRoleError()
        # check if there's enough product available
        product = await self.product_repository.get_product_for_update(
            request.product_id
        )
        if not product:
            log.info(f"Product {request.product_id} not found")
            raise ProductNotFoundError()
        if product.amount_available < request.amount:
            log.info(
                f"Not enough product available. Requested: {request.amount} in stock: {product.amount_available}"
            )
            raise NotEnoughProductError()

        total_price = product.cost * request.amount
        if buyer.deposit < total_price:
            log.info(
                f"Not enough money deposited. Requested: {total_price} in deposit: {buyer.deposit}"
            )
            raise NotEnoughMoneyError()
        # check if there's enough change available
        calculate_amount_after = buyer.deposit - total_price

        current_coins_in_machine = await self.vending_machine.get_coins_for_update()
        # calculate_amount_spent
        log.info(f"Calculating change for {calculate_amount_after}")
        try:
            calculated_change = await machine.calculate_change(
                current_coins=current_coins_in_machine, amount=calculate_amount_after
            )
        except NotEnoughChangeError:
            log.info(
                f"Not enough change in machine. Current coins in machine: {current_coins_in_machine}"
            )
            raise NotEnoughChangeError()

        log.info(
            f"Calculating change for change:{calculate_amount_after} coins:{calculated_change}  "
        )

        # then update the product amount available
        product = await self.product_repository.buy_product(
            request.product_id, request.amount
        )
        res = await self.user_repository.decrease_deposit(request.user_id, total_price)

        log.info(
            f"succesfully bought product {product.product_name} for user {buyer} with total price {total_price} and change {calculated_change}"
        )
        return BuyProductSummary(
            total_spent=total_price,
            product_name=product.product_name,
            change=calculated_change,
        )

    async def reset_user_deposit(self, user_id: UUID) -> None:
        current_user = await self.user_repository.get_for_update(user_id)
        current = current_user.deposit
        if current_user.role == "seller":
            raise InvalidRoleError()
        if current > 0:
            coins_in_machine = await self.vending_machine.get_coins_for_update()
            calculated_change = await machine.calculate_change(
                current_coins=coins_in_machine, amount=current
            )
            await self.vending_machine.remove_coins(calculated_change)
            await self.user_repository.reset_deposit(user_id)

            log.info(
                f"Reset deposit for user {user_id} to 0 and removed {calculated_change} from vending machine"
            )

            return
        else:
            log.info("Nothing to reset")

        return


async def get_vending_service(
    user_repository: UserRepository = Depends(get_user_repository),
    product_repository: ProductRepository = Depends(get_product_repository),
    vending_machine: machine.VendingMachine = Depends(machine.get_vending_machine),
):
    return VendingService(
        user_repository=user_repository,
        product_repository=product_repository,
        vending_machine=vending_machine,
    )
