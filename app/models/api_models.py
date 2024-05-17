from typing import List
from pydantic import BaseModel, Field, validator
from app.models.dynamic_models import PyObjectId


class Product(BaseModel):
    id: str
    name: str
    price: float
    
class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(BaseModel):
    id: str

    items: List[OrderItem]
    customer_id: str
    
    class Config:
        json_encoders = {
            PyObjectId: lambda oid: str(oid)
        }
        
class Customer(BaseModel):
    id: str
    name: str
    contact: str
    
