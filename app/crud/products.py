from app.database import Database


# Product operations

async def create_product(product):
    await Database.client.app_db.products.insert_one(product.dict())

async def read_product(product_id):
    return await Database.client.app_db.products.find_one({"id": product_id})

async def update_product(product_id, product):
    await Database.client.app_db.orders.update_one({"id": product_id}, {"$set": product.dict()})
    return await read_product(product_id)

async def delete_product(product_id):
    result = await Database.client.app_db.products.delete_one({"id": product_id})
    return result.deleted_count > 0

