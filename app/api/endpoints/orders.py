from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.models.api_models import Order
from app.crud.orders import create_order, read_order, update_order, delete_order, get_all_orders

router = APIRouter()

@router.post("/", response_model=Order)
async def create_order_endpoint(order: Order):
    await create_order(order)
    return order

@router.get("/{order_id}", response_model=Order)
async def read_order_endpoint(order_id: str):
    order = await read_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=List[Order])
async def read_all_orders(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), sort_by_id: int = Query(None)):
    """
    Retrieve all orders with pagination.
    :param skip: Number of records to skip (for pagination).
    :param limit: Maximum number of records to return.
    :return: List of orders.
    """
    orders = await get_all_orders(skip, limit, sort_by_id)
    return orders

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