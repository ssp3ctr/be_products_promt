from typing import List
from fastapi import APIRouter, Depends
from app.models.api_models import Order
from app.crud.generic import GenericCRUD
from app.database import Database
from app.crud.orders import read_order

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
    return await crud.read({"id": order_id})

# specific method from generic
@router.get("/specific_read_generic/{customer_id}", response_model=Order)
async def get_order(customer_id: str, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.specific_read({"customer_id": customer_id})

# specific method from ourders crud
@router.get("/specific_read/{customer_id}", response_model=Order)
async def get_order(customer_id: str, crud: GenericCRUD = Depends(get_order_crud)):
    return await read_order({"customer_id": customer_id})

@router.get("/", response_model=List[Order])
async def list_orders(skip: int = 0, limit: int = 10, sort_field: str = None, sort_direction: int =1, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.retrieve({}, skip=skip, limit=limit, sort_field=sort_field, sort_direction=sort_direction)

@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, order_data: dict, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.update({"id": order_id}, order_data)

@router.delete("/{order_id}")
async def delete_order(order_id: str, crud: GenericCRUD = Depends(get_order_crud)):
    return await crud.delete({"id": order_id})