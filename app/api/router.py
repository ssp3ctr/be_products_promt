from fastapi import APIRouter
from app.api.endpoints import customers, products, orders

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])