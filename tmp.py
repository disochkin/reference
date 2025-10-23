from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    quantity = Column(Integer)

    # обратная связь с Order
    order = relationship("Order", back_populates="order_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # связь с OrderItem
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")



# https://disk.yandex.ru/d/pkh-RGwTsHi_Mg