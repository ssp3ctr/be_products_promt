from fastapi import APIRouter, HTTPException, status, Path , Request, Depends
from app.models.dynamic_models import DictionaryItem
from app.database import Database
from bson import ObjectId
from app.crud.generic import DictionaryGenericCRUD

router = APIRouter()

def get_crud(request: Request):
    collection_name = request.path_params['collection_name']
    return DictionaryGenericCRUD(Database.database, f"dictionaries_{collection_name}")

@router.post("/{collection_name}")
async def create_dictionary_item(data: dict, crud: DictionaryGenericCRUD = Depends(get_crud)):
    return await crud.create(data)
    
@router.get("/{collection_name}/{item_id}")
async def get_dictionary_item(item_id: str, crud: DictionaryGenericCRUD = Depends(get_crud)):
    item = await crud.retrieve(item_id)
    if item:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
#@router.get("/{collection_name}/{item_id}")
#async def get_dictionary_item(item_id: str, crud: DictionaryGenericCRUD = Depends(get_crud)):
#   return await crud.retrieve(item_id)

@router.put("/{collection_name}/{item_id}")
async def update_dictionary_item(item_id: str, item: DictionaryItem, crud: DictionaryGenericCRUD = Depends(get_crud)):
    update_result = await crud.update(item_id, item.model_dump(by_alias=True))
    if update_result.modified_count:
        return {"status": "Item updated", "id": item_id}
    else:
        raise HTTPException(status_code=404, detail="Item not found or no update made")

@router.delete("/{collection_name}/{item_id}")
async def delete_dictionary_item(item_id: str, crud: DictionaryGenericCRUD = Depends(get_crud)):
    delete_result = await crud.delete(item_id)
    if delete_result.deleted_count:
        return {"status": "Item deleted", "id": item_id}
    else:
        raise HTTPException(status_code=404, detail="Item not found")