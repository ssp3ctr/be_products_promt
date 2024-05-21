from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.dynamic_models import DictionaryItem
from app.database import Database
from app.crud.generic import DictionaryGenericCRUD
from typing import List

router = APIRouter()

def get_crud(request: Request):
    collection_name = request.path_params['collection_name']
    return DictionaryGenericCRUD(Database.database, f"dictionaries_{collection_name}")

@router.post("/{collection_name}")
async def create_dictionary_item(data: dict, crud: DictionaryGenericCRUD = Depends(get_crud)):
    return await crud.create(data)

@router.get("/{collection_name}", response_model=List[DictionaryItem])
async def list_dictionaries(collection_name: str, skip: int = 0, limit: int = 10, sort_field: str = None, sort_direction: int = 1, crud: DictionaryGenericCRUD = Depends(get_crud)):
    return await crud.retrieve({}, skip=skip, limit=limit, sort_field=sort_field, sort_direction=sort_direction)

@router.get("/{collection_name}/{item_id}")
async def get_dictionary_item(item_id: str, crud: DictionaryGenericCRUD = Depends(get_crud)):
    return await crud.read_by_id(item_id)

@router.put("/{collection_name}/{item_id}")
async def update_dictionary_item(item_id: str, item: DictionaryItem, crud: DictionaryGenericCRUD = Depends(get_crud)):
    return await crud.update(item_id, item.dict(by_alias=True))

@router.delete("/{collection_name}/{item_id}")
async def delete_dictionary_item(item_id: str, crud: DictionaryGenericCRUD = Depends(get_crud)):
    return await crud.delete(item_id)