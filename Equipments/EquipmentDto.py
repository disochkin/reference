from pydantic import BaseModel, Field

from Supplier.SupplierDto import SupplierDtoFormResponseNameCountry


class EquipmentDtoCreate(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    supplier_id: int

class EquipmentDtoResponse(BaseModel):
    id: int
    name: str
    price: int
    supplier: SupplierDtoFormResponseNameCountry | None = None
    model_config = {
        "from_attributes": True
    }

class EquipmentDtoResponseTable(BaseModel):
    id: int
    name: str
    price: int
    model_config = {
        "from_attributes": True
    }

class EquipmentUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
