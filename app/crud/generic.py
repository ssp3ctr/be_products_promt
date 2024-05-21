from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from bson import ObjectId

class GenericCRUD:
    def __init__(self, collection):
        self.collection = collection

    async def create(self, data):
        try:
            result = await self.collection.insert_one(data)
            if result.acknowledged:
                data['_id'] = str(result.inserted_id)
                return data
            else:
                raise HTTPException(status_code=500, detail="Failed to create item")
        except DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Document with this ID already exists")

    async def read_by_id(self, item_id):
        document = await self.collection.find_one({"_id": ObjectId(item_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Item not found")
        document['_id'] = str(document['_id'])
        return document
    
    async def read(self, query):
        document = await self.collection.find_one(query)
        return document
    
    async def retrieve(self, query, skip=0, limit=10, sort_field=None, sort_direction=1):
        sort_criteria = [(sort_field, sort_direction)] if sort_field else None
        cursor = self.collection.find(query)
        if sort_criteria:
            cursor = cursor.sort(sort_criteria)
        cursor = cursor.skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return documents

    async def update(self, item_id, update_data):
        update_result = await self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No updates made or item not found")
        return await self.retrieve(item_id)

    async def delete(self, item_id):
        result = await self.collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"status": "Item deleted", "id": str(item_id)}
    
class DictionaryGenericCRUD(GenericCRUD):
    def __init__(self, db, collection_name):
        super().__init__(db[f"dictionaries_{collection_name}"])