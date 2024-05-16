from fastapi import APIRouter, HTTPException
from app.models.api_models import Customer
from app.crud.customers import create_customer, read_customer, update_customer, delete_customer

router = APIRouter()

@router.post("/", response_model=Customer)
async def create_customer_endpoint(customer: Customer):
    await create_customer(customer)
    return customer

@router.get("/{customer_id}", response_model=Customer)
async def read_customer_endpoint(customer_id: str):
    customer = await read_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
async def update_customer_endpoint(customer_id: str, customer: Customer):
    updated_customer = await update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

@router.delete("/{customer_id}")
async def delete_customer_endpoint(customer_id: str):
    success = await delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"status": "deleted"}
