from typing import List
from fastapi import APIRouter, Depends
from app.models.api_models import Customer
from app.crud.generic import GenericCRUD
from app.database import Database


router = APIRouter()

# Dependency to ensure database is connected and get CRUD object
async def get_crud() -> GenericCRUD:
    await Database.connect()  # Ensure connection if not already done
    return GenericCRUD(Database.customers)

@router.post("/", response_model=Customer)
async def create_customer(data: dict, crud: GenericCRUD = Depends(get_crud)):
    return await crud.create(data)

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str, crud: GenericCRUD = Depends(get_crud)):
    return await crud.read({"id": customer_id})

@router.get("/", response_model=List[Customer])
async def list_customers(skip: int = 0, limit: int = 10, sort_field: str = None, sort_direction: int =1, crud: GenericCRUD = Depends(get_crud)):
    return await crud.retrieve({}, skip=skip, limit=limit, sort_field=sort_field, sort_direction=sort_direction)

@router.put("/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, data: dict, crud: GenericCRUD = Depends(get_crud)):
    return await crud.update({"id": customer_id}, data)

@router.delete("/{customer_id}")
async def delete_customer(customer_id: str, crud: GenericCRUD = Depends(get_crud)):
    return await crud.delete({"id": customer_id})