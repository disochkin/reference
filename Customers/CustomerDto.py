import enum
from datetime import datetime

from pydantic import BaseModel

from OrderItem.OrderItemDto import OrderItemDto
from OrderItem.OrderItemModel import OrderItem

class CustomerDtoShort(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }
