from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import select

from app.db.sql.models import Product
from app.deps import get_session
from app.products.models import ProductCreate, ProductRead, ProductUpdate


class ProductRepository(ABC):
    @abstractmethod
    def get_all_products(self) -> List[ProductRead]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        pass

    @abstractmethod
    def create_product(self, product: ProductCreate) -> ProductRead:
        pass

    @abstractmethod
    def update_product(
        self, product_id: int, product: ProductUpdate
    ) -> Optional[ProductRead]:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> Optional[ProductRead]:
        pass


class SQLProductRepository:
    async def get_all_products(self) -> List[ProductRead]:
        async with get_session() as db_session:
            products = await db_session.execute(select(Product))
            return [
                ProductRead(model_validate=product) for product in products.scalars()
            ]

    async def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        async with get_session() as db_session:
            product = await db_session.execute(select(Product).filter_by(id=product_id))
            product = product.scalar_one_or_none()
            if product:
                return ProductRead(model_validate=product)
            return None

    async def create_product(self, product_create: ProductCreate) -> ProductRead:
        async with get_session() as db_session:
            new_product = Product(**product_create.dict())
            db_session.add(new_product)
            await db_session.commit()
            return ProductRead(model_validate=new_product)

    async def update_product(
        self, product_id: int, product_update: ProductUpdate
    ) -> Optional[ProductRead]:
        async with get_session() as db_session:
            existing_product = await db_session.execute(
                select(Product).filter_by(id=product_id)
            )
            existing_product = existing_product.scalar_one_or_none()
            if existing_product:
                for key, value in product_update.dict().items():
                    setattr(existing_product, key, value)
                await db_session.commit()
                return ProductRead(model_validate=existing_product)
            return None

    async def delete_product(self, product_id: int) -> Optional[ProductRead]:
        async with get_session() as db_session:
            existing_product = await db_session.execute(
                select(Product).filter_by(id=product_id)
            )
            existing_product = existing_product.scalar_one_or_none()
            if existing_product:
                db_session.delete(existing_product)
                await db_session.commit()
                return ProductRead(model_validate=existing_product)
            return None
