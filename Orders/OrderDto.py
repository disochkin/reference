import enum
from datetime import datetime
from typing import List

from pydantic import BaseModel, field_serializer, computed_field

from Customers.CustomerDto import CustomerDtoShort
from Managers.ManagerDto import ManagerDtoShort
from OrderItem.OrderItemDto import OrderItemDto
from OrderItem.OrderItemModel import OrderItem

class OrderDtoCreate(BaseModel):
    manager_id: int
    customer_id: int

class OrderDtoResponse(BaseModel):
    id: int
    created_at: datetime
    manager_id: int
    customer_id: int

class OrderDtoResponseFull(BaseModel):
    id: int
    created_at: datetime
    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime, _info):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    manager: ManagerDtoShort | None = None
    customer: CustomerDtoShort | None = None
    order_items: List[OrderItemDto] = []
    status: str
    @computed_field
    @property
    def total_amount(self) -> float:
        """Рассчитываем общую сумму всех позиций заказа"""
        return sum(item.total_price for item in self.order_items)
    model_config = {
        "from_attributes": True
    }

class OrderDtoResponseTable(BaseModel):
    id: int
    created_at: datetime
    manager: ManagerDtoShort | None = None
    customer: CustomerDtoShort | None = None
    status: str
    total_sum: float | None = None # сумма заказа
    model_config = {
        "from_attributes": True
    }

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime, _info):
        return value.strftime("%Y-%m-%d %H:%M:%S")

class StatusEnum(str, enum.Enum):
    new = "new"
    complete = "complete"
