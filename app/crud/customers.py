from app.database import Database


# Customer operations

async def create_customer(customer):
    await Database.client.mydb.customers.insert_one(customer.dict())

async def read_customer(customer_id):
    return await Database.client.mydb.customers.find_one({"id": customer_id})

async def update_customer(customer_id, customer):
    await Database.client.mydb.customers.update_one({"id": customer_id}, {"$set": customer.dict()})
    return await read_customer(customer_id)

async def delete_customer(customer_id):
    result = await Database.client.mydb.customers.delete_one({"id": customer_id})
    return result.deleted_count > 0