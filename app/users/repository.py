from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import delete, select, update
from app.db.sql.models import User

from app.users.models import UserCreate, UserRead, UserDeposit, UserUpdate


class UserRepository(ABC):
    @abstractmethod
    async def delete(self, id: UUID):
        pass

    @abstractmethod
    async def update_current_user(
        self, current_user: User, update_request: UserUpdate
    ) -> Optional[UserRead]:
        pass

    @abstractmethod
    async def register_new_user(self, new_user: UserCreate) -> UserRead:
        pass

    @abstractmethod
    async def deposit_coins(self, request: UserDeposit):
        pass

    @abstractmethod
    async def reset_deposit(self, user_id: UUID):
        pass


class SQLUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_user(self, id: UUID):
        """Delete current user"""
        await self.session.execute(delete(User).where(User.id == id))
        await self.session.commit()

    async def update_current_user(
        self, current_user: User, update_request: UserUpdate
    ) -> Optional[UserRead]:
        """Update current user"""
        await self.session.execute(
            update(User)
            .where(User.id == current_user.id)
            .values(**update_request.model_dump(exclude_unset=True))
        )
        await self.session.commit()
        usr = await self.session.execute(select(User).where(User.id == current_user.id))
        return UserRead.model_validate(usr)

    async def register_new_user(self, new_user: UserCreate) -> UserRead:
        """Create new user"""
        result = await self.session.execute(
            select(User).where(User.username == new_user.username)
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise ValueError("Cannot use this username")

        user = User(
            username=new_user.username,
            password=new_user.password,
            role=new_user.role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserRead.model_validate(user)

    async def deposit_coins(self, request: UserDeposit):
        """Deposit coins - make sure to use the correct coin values and lock the table for that"""

        user = (
            await self.session.execute(
                select(User).where(User.id == request.user_id).with_for_update()
            )
            .scalar()
            .first()
        )
        if user:
            await self.session.execute(
                update(User)
                .where(User.id == request.user_id)
                .values(deposit=User.deposit + request.amount)
            )
        else:
            raise ValueError("User not found")
        await self.session.commit()
        await self.session.refresh(user)
        return UserRead.model_validate(user)

    @abstractmethod
    async def reset_deposit(self, id: UUID):
        await self.session.execute(update(User).where(User.id == id).values(deposit=0))
        await self.session.commit()
        return {"message": "Vending machine reset successfully"}
