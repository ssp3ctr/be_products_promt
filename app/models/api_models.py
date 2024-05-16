from typing import List
from pydantic import BaseModel, Field, validator
from bson import ObjectId

class PyObjectId(ObjectId):
   
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_name: str):
        return {"type": "string", "format": "objectid"}


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
    
