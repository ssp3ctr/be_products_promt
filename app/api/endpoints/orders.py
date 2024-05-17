from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from app.models.api_models import Order
from app.crud.orders import create_order, read_order, update_order, delete_order, get_all_orders
from app.crud.generic import GenericCRUD
from app.database import Database

router = APIRouter()

# Dependency to ensure database is connected and get CRUD object
async def get_order_crud() -> GenericCRUD:
    await Database.connect()  # Ensure connection if not already done
    return GenericCRUD(Database.orders)

@router.post("/", response_model=Order)
async def create_order(order_data: dict, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.create(order_data)

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.read_order({"id": order_id})

@router.get("/", response_model=List[Order])
async def list_orders(skip: int = 0, limit: int = 10, sort_field: str = None, sort_direction: int =1, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.retrieve({}, skip=skip, limit=limit, sort_field=sort_field, sort_direction=sort_direction)

@router.put("/{order_id}", response_model=Order)
async def update_order_endpoint(order_id: str, order: Order):
    updated_order = await update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}")
async def delete_order_endpoint(order_id: str):
    success = await delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": "deleted"}