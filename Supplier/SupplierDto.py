from xmlrpc.client import DateTime

from pydantic import BaseModel

# class OrderDtoCreate(BaseModel):
#     name: str
#     price: int

class SupplierDtoFormResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class SupplierDtoFormResponseNameCountry(BaseModel):
    name: str
    country: str
    model_config = {
        "from_attributes": True
    }