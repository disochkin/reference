import enum
from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemDtoCreate(BaseModel):
    order_id: int
    equipment_id: int
    quantity: int = Field(..., gt=0)

class OrderItemDto(BaseModel):
    id: int
    equipment_id: int
    quantity: int
    price_per_unit: float

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
