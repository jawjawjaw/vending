# - Implement CRUD for a product model (GET can be called by anyone, while POST, PUT and DELETE can be called only by the seller user who created the product)
# based on my previous users.py file, I have created a products.py file in the same directory

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api import deps
from app.api.dependencies import get_product_repository
from app.db.sql.models import User
from app.models.product import Product, ProductCreate, ProductUpdate
from app.repositories.product import ProductRepository

router = APIRouter()


#


# GET /products - Get all products
@router.get("/products")
def get_all_products(product_repo: ProductRepository = Depends(get_product_repository)):
    products = product_repo.get_all_products()
    return products


@router.post("/products")
def create_product(
    product: ProductCreate,
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(deps.get_current_user),
):
    product.seller_id = current_user.id
    created_product = product_repo.create_product(product)
    return created_product


@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductUpdate,
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(deps.get_current_user),
):
    existing_product = product_repo.get_product_by_id(product_id)
    if existing_product.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this product.",
        )
    updated_product = product_repo.update_product(product_id, product)
    return updated_product


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    product_repo: ProductRepository = Depends(get_product_repository),
    current_user: User = Depends(deps.get_current_user),
):
    existing_product = product_repo.get_product_by_id(product_id)
    if existing_product.seller_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this product.",
        )
    deleted_product = product_repo.delete_product(product_id)
    return deleted_product
