from app.database import Database
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException

# Order operations

# specific order reading
async def read_order(order_id):
    """Retrieves a single order by its ID."""
    return await Database.orders.find_one({"id": order_id})

