from pydantic.v1 import validator
from sqlalchemy import Column, ForeignKey, Integer, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id") ,nullable=False)

    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")

    equipment = relationship("Equipment", back_populates="order_items")

    # уникальность 2х стобцов
    __table_args__ = (
        UniqueConstraint("order_id", "equipment_id", name="order_id_equipment_id_constraint"),
    )

    def __init__(self, order_id, equipment_id, quantity, price_per_unit):
        self.order_id=order_id
        self.equipment_id=equipment_id
        self.quantity=quantity
        self.price_per_unit=price_per_unit


