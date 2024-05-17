from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    database = None
    orders = None
    products = None
    customers = None
    orders_collection = None

    @staticmethod
    async def connect():
        db_url = os.getenv('DATABASE_URL')
        db_name = os.getenv('DATABASE_NAME')
        orders_collection = os.getenv('ORDERS_COLLECTION')
        product_collection = os.getenv('PRODUCTS_COLLECTION')
        customers_collection = os.getenv('CUSTOMERS_COLLECTION')

        Database.database = AsyncIOMotorClient(db_url)[db_name]
        Database.orders = Database.database[orders_collection]
        Database.products = Database.database[product_collection]
        Database.customers = Database.database[customers_collection]

    @staticmethod
    async def disconnect():
        Database.client.close()