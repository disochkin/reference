import enum
from datetime import datetime

from pydantic import BaseModel, Field, computed_field
from pydantic.v1 import validator

from Equipments.EquipmentDto import EquipmentShortDescription


class OrderItemDtoCreate(BaseModel):
    order_id: int
    equipment_id: int
    quantity: int = Field(..., gt=0)

class OrderItemDto(BaseModel):
    id: int
    equipment: EquipmentShortDescription | None = None
    quantity: int
    price_per_unit: float

    @computed_field
    @property
    def total_price(self) -> float:
        """Вычисляет общую сумму строки заказа."""
        return self.quantity * self.price_per_unit
    class Config:
        from_attributes = True  # вместо устаревшего from_orm=True


#
# class OrderDtoResponse(BaseModel):
#     id: int
#     created_at: datetime
#     manager_id: int
#     customer_id: int
#
# class StatusEnum(str, enum.Enum):
#     new = "new"
#     complete = "complete"
