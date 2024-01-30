from abc import ABC, abstractmethod
import uuid
from fastapi import Depends
from jwt import InvalidTokenError
from sqlalchemy import select, update
from app.core.config import settings
from app.db.sql.session import get_session
from app.users.models import AVAILABLE_COINS
from app.errors import NotEnoughChangeError
from app.vending.models import Change
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.sql.models import VendingMachine as VendingMachineModel


class VendingMachine(ABC):
    @abstractmethod
    async def get_coins_for_update(self):
        pass

    @abstractmethod
    async def set_coins(self, c: Change):
        pass

    @abstractmethod
    async def reset_vending_machine(self):
        pass

    @abstractmethod
    async def remove_coins(self, to_remove: Change) -> Change:
        pass

    @abstractmethod
    async def add_coin(self, coin: int) -> Change:
        pass


class SQLVendingMachine:
    def __init__(
        self,
        session: AsyncSession,
        machine_id: uuid.UUID = uuid.UUID("00000000-0000-0000-0000-000000000000"),
    ):
        self.session = session
        self.machine_id = machine_id

    async def get_coins_for_update(self):
        # get the coins from the db
        q = await self.session.execute(
            select(VendingMachineModel)
            .where(VendingMachineModel.id == self.machine_id)
            .with_for_update()
        )
        coins = q.scalars().first()
        return Change.model_validate(coins.status)

    async def set_coins(
        self,
        c: Change,
    ):
        # use VendingMachineModel to deposit the coins
        await self.session.execute(
            update(VendingMachineModel)
            .where(VendingMachineModel.id == self.machine_id)
            .values(status=c.root)
        )
        await self.session.commit()

    async def reset_vending_machine(self):
        # use VendingMachineModel to reset the vending machine
        await self.session.execute(
            update(VendingMachineModel)
            .where(VendingMachineModel.id == self.machine_id)
            .values(status={c: 0 for c in AVAILABLE_COINS})
        )
        await self.session.commit()

    async def remove_coins(self, to_remove: Change) -> Change:
        current = await self.get_coins_for_update()
        for k, v in to_remove.root.items():
            current[k] -= v
            if current[k] < 0:
                await self.session.rollback()
                raise NotEnoughChangeError()
        c = Change(root=current)
        await self.set_coins(c)

        return c

    async def add_coin(self, coin: int) -> Change:
        if coin not in AVAILABLE_COINS:
            raise InvalidTokenError()
        current = await self.get_coins_for_update()
        current.root[coin] += 1

        await self.set_coins(current)
        return current


def get_vending_machine_id():
    return settings.VENDING_MACHINE_ID


def get_vending_machine(
    session: AsyncSession = Depends(get_session),
    machine_id: uuid.UUID = Depends(get_vending_machine_id),
):
    return SQLVendingMachine(session, machine_id)


async def calculate_change(current_coins: Change, amount: int) -> Change:
    # Only calculate - do not update yet
    # init empty change dict
    change = Change(root={c: 0 for c in AVAILABLE_COINS})

    # iterate and get the largest first
    for coin in sorted(AVAILABLE_COINS, reverse=True):
        # check if the coin value is not too big and if there's enough coins of this type
        while amount >= coin and current_coins.root[coin] > 0:
            change.root[coin] += 1
            amount -= coin
            current_coins.root[coin] -= 1
    # should be 0 after the loop
    if amount > 0:
        print(amount)
        raise NotEnoughChangeError()
    return change
