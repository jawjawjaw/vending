# class ProductRepositoryABC(ABC):
#     @abstractmethod
#     def get_all_products(self) -> List[Product]:
#         pass

#     @abstractmethod
#     def get_product_by_id(self, product_id: int) -> Optional[Product]:
#         pass

#     @abstractmethod
#     def create_product(self, product: ProductCreate) -> Product:
#         pass

#     @abstractmethod
#     def update_product(self, product_id: int, product: ProductUpdate) -> Optional[Product]:
#         pass

#     @abstractmethod
#     def delete_product(self, product_id: int) -> Optional[Product]:
#         pass


# class ProductRepository(ProductRepositoryABC):
#     def __init__(self):
#         # Initialize any necessary variables or connections here
#         pass

#     def get_all_products(self) -> List[Product]:
#         # Implement the logic to retrieve all products from the database or any other data source
#         pass

#     def get_product_by_id(self, product_id: int) -> Optional[Product]:
#         # Implement the logic to retrieve a specific product by its ID from the database or any other data source
#         pass

#     def create_product(self, product: ProductCreate) -> Product:
#         # Implement the logic to create a new product in the database or any other data source
#         pass

#     def update_product(self, product_id: int, product: ProductUpdate) -> Optional[Product]:
#         # Implement the logic to update a product in the database or any other data source
#         pass

#     def delete_product(self, product_id: int) -> Optional[Product]:
#         # Implement the logic to delete a product from the database or any other data source
#         pass

# class BaseWithTimestamps(Base):
#     __abstract__ = True  # This ensures this base class is not mapped to a table
#     id = Column(
#         String(36),
#         primary_key=True,
#         default=str(uuid.uuid4()),
#         nullable=False,
#         unique=True,
#     )

#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = Column(
#         DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
#     )


# class User(BaseWithTimestamps):
#     __tablename__ = "users"

#     username = Column(
#         String(32), primary_key=True, nullable=False, unique=True, index=True
#     )
#     password = Column(String(128), nullable=False)
#     deposit = Column(Integer, nullable=False, default=0)
#     role = Column(String(32), nullable=False)
#     products = relationship("Product", back_populates="seller")


# class Product(BaseWithTimestamps):
#     __tablename__ = "products"

#     amountAvailable = Column(Integer, nullable=False)
#     cost = Column(Integer, nullable=False)
#     productName = Column(String(32), nullable=False)
#     # seller_id is foreign key to Users table
#     seller_id = Column(String(32), ForeignKey("users.id"), nullable=False)

#     # Define a relationship to the User model
#     seller = relationship("User", back_populates="products")


from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    amount_available: int
    cost: int
    product_name: str
    seller_id: str


class ProductUpdate(BaseModel):
    amount_available: Optional[int]
    cost: Optional[int]
    product_name: Optional[str]


class ProductRead(ProductCreate):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
