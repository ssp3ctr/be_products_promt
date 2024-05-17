from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException

class GenericCRUD:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, data):
        """Create a document and handle duplicate key error."""
        try:
            result = await self.collection.insert_one(data)
            return result.inserted_id
        except DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Document with this ID already exists")

    async def retrieve(self, query, skip=0, limit=10, sort_field=None, sort_direction=1):
        """Retrieve documents with optional sorting and pagination."""
        sort_criteria = [(sort_field, sort_direction)] if sort_field else None
        cursor = self.collection.find(query)
        if sort_criteria:
            cursor = cursor.sort(sort_criteria)
        cursor = cursor.skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return documents

    async def read_order(self, query):
        """Retrieve a single document by query."""
        document = await self.collection.find_one(query)
        return document

    async def update(self, query, update_data):
        """Update a document and return the updated document."""
        update_result = await self.collection.update_one(query, {"$set": update_data})
        if update_result.modified_count == 0:
            return None
        return await self.find_one(query)

    async def delete(self, query):
        """Deletes a document and returns True if the operation was successful."""
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
