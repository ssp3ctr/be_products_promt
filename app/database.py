from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    async def connect(cls, uri):
        cls.client = AsyncIOMotorClient(uri)

    @classmethod
    async def disconnect(cls):
        cls.client.close()