"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class BaseWithTimestamps(Base):
    __abstract__ = True  # This ensures this base class is not mapped to a table
    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        nullable=False,
        unique=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(BaseWithTimestamps):
    __tablename__ = "users"

    username = Column(
        String(32), primary_key=True, nullable=False, unique=True, index=True
    )
    password = Column(String(128), nullable=False)
    deposit = Column(Integer, nullable=False, default=0)
    role = Column(String(32), nullable=False)
    products = relationship("Product", back_populates="seller")


class Product(BaseWithTimestamps):
    __tablename__ = "products"

    product_available = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    product_name = Column(String(32), nullable=False)
    # seller_id is foreign key to Users table
    seller_id = Column(String(32), ForeignKey("users.id"), nullable=False)

    # Define a relationship to the User model
    seller = relationship("User", back_populates="products")
