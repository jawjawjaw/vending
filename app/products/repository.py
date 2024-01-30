from abc import ABC, abstractmethod
from typing import List, Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.db.sql.models import Product
from app.db.sql.session import get_session
from app.errors import NotEnoughProductError, ProductNotFoundError
from app.products.models import ProductCreate, ProductRead, ProductUpdate


class ProductRepository(ABC):
    @abstractmethod
    async def get_all_products(self) -> List[ProductRead]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        pass

    @abstractmethod
    async def get_product_for_update(self, product_id: int) -> Optional[ProductRead]:
        pass

    @abstractmethod
    async def create_product(self, product: ProductCreate) -> ProductRead:
        pass

    @abstractmethod
    async def update_product(
        self, product_id: int, product: ProductUpdate
    ) -> Optional[ProductRead]:
        pass

    @abstractmethod
    async def delete_product(self, product_id: int) -> Optional[ProductRead]:
        pass

    @abstractmethod
    async def buy_product(self, product_id: int, amount: int) -> Optional[ProductRead]:
        pass


class SQLProductRepository:
    def __init__(self, session: AsyncSession):
        self.db_session = session or get_session()

    async def get_all_products(self) -> List[ProductRead]:
        products = await self.db_session.execute(select(Product))
        return [
            ProductRead.model_validate(product) for product in products.scalars().all()
        ]

    async def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        product = await self.db_session.execute(
            select(Product).filter_by(id=product_id)
        )
        product = product.scalar_one_or_none()
        if product:
            return ProductRead.model_validate(product)
        return None

    async def create_product(self, product_create: ProductCreate) -> ProductRead:
        new_product = Product(**product_create.model_dump())
        self.db_session.add(new_product)
        await self.db_session.commit()
        return ProductRead.model_validate(new_product)

    async def update_product(
        self, product_id: int, product_update: ProductUpdate
    ) -> Optional[ProductRead]:
        existing_product = await self.db_session.execute(
            select(Product).filter_by(id=product_id).with_for_update()
        )
        existing_product = existing_product.scalar_one_or_none()
        if existing_product:
            for key, value in product_update.model_dump().items():
                setattr(existing_product, key, value)
            await self.db_session.commit()
            return ProductRead.model_validate(existing_product)
        return None

    async def delete_product(self, product_id: int) -> Optional[ProductRead]:
        existing_product = await self.db_session.execute(
            select(Product).filter_by(id=product_id)
        )
        existing_product = existing_product.scalar_one_or_none()
        if existing_product:
            await self.db_session.delete(existing_product)
            await self.db_session.commit()
            return ProductRead.model_validate(existing_product)

        return None

    async def get_product_for_update(self, product_id: int) -> Optional[ProductRead]:
        product = await self.db_session.execute(
            select(Product).filter_by(id=product_id).with_for_update()
        )
        product = product.scalar_one_or_none()
        if product:
            return ProductRead.model_validate(product)
        return None

    async def buy_product(self, product_id: int, amount: int) -> Optional[ProductRead]:
        product = await self.db_session.execute(
            select(Product).filter_by(id=product_id).with_for_update()
        )
        product = product.scalar_one_or_none()
        if product:
            product.amount_available -= amount
            if product.amount_available < 0:
                await self.db_session.rollback()
                return NotEnoughProductError()
            await self.db_session.commit()
            return ProductRead.model_validate(product)
        raise ProductNotFoundError()


async def get_product_repository(session=Depends(get_session)) -> ProductRepository:
    return SQLProductRepository(session=session)
