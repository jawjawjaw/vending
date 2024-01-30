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

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class BaseWithTimestamps(Base):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
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
    vending_id = Column(
        UUID,
        ForeignKey("vending_machines.id"),
        nullable=False,
        default=uuid.UUID("00000000-0000-0000-0000-000000000000"),
    )

    products = relationship("Product", back_populates="seller")
    vending = relationship("VendingMachine", back_populates="users")


class Product(BaseWithTimestamps):
    __tablename__ = "products"

    amount_available = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    product_name = Column(String(64), nullable=False)
    # seller_id is foreign key to Users table
    seller_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    # Define a relationship to the User model
    seller = relationship("User", back_populates="products")

    vending_id = Column(
        UUID,
        ForeignKey("vending_machines.id"),
        nullable=False,
        default=uuid.UUID("00000000-0000-0000-0000-000000000000"),
    )
    vending = relationship("VendingMachine", back_populates="products")


class VendingMachine(BaseWithTimestamps):
    __tablename__ = "vending_machines"
    # json field
    status = Column(JSON, nullable=False)
    products = relationship("Product", back_populates="vending")
    users = relationship("User", back_populates="vending")
