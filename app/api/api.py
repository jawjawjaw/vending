from fastapi import APIRouter

from app.api.endpoints import auth, products, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/user", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
