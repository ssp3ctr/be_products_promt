from pydantic import BaseModel, Extra
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
    
class DictionaryItem(BaseModel):
    id: int  # You might still want to ensure some core fields are defined
    name: str

    class Config:
        extra = Extra.allow  # This allows the model to accept any additional fields
        
class TreeDictionaryItem(BaseModel):
    id: int  # You might still want to ensure some core fields are defined
    name: str
   

    class Config:
        extra = Extra.allow  # This allows the model to accept any additional fields
       
        
