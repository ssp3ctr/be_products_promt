from app.database import Database
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException

# Order operations

async def create_order(order):
    """Creates an order and handles duplicate key error."""
    try:
        order_data = order.dict()
        result = await Database.client.app_db.orders.insert_one(order_data)
        return result.inserted_id
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Order with this ID already exists")

async def get_all_orders(skip: int, limit: int, sort_field: str = None, sort_direction: int = 1):
    """Retrieves all orders with optional sorting and pagination."""
    sort_criteria = [(sort_field, sort_direction)] if sort_field else None
    query = Database.client.app_db.orders.find()
    
    if sort_criteria:
        query = query.sort(sort_criteria)
    
    query = query.skip(skip).limit(limit)
    orders = await query.to_list(length=limit)
    return orders

async def read_order(order_id):
    """Retrieves a single order by its ID."""
    return await Database.client.app_db.orders.find_one({"id": order_id})

async def update_order(order_id, order):
    """Updates an order and returns the updated document."""
    update_result = await Database.client.app_db.orders.update_one({"id": order_id}, {"$set": order.dict()})
    if update_result.modified_count == 0:
        return None
    return await read_order(order_id)

async def delete_order(order_id):
    """Deletes an order and returns True if the operation was successful."""
    result = await Database.client.app_db.orders.delete_one({"id": order_id})
    return result.deleted_count > 0
