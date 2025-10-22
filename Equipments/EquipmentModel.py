from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Внешний ключ на Supplier поставщика
    supplier_id = Column(Integer, ForeignKey("supplier.id", ondelete="RESTRICT"),nullable=False)

    supplier = relationship("Supplier", back_populates="equipment")

    # связь многие ко многим с заявками
    order_items  = relationship("OrderItem", back_populates="equipment")

    def __init__(self, name: str, price: int, supplier_id: int):
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
