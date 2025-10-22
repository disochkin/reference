
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String, default="new", nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('new', 'complete')", name="status_check"),
    )

    #
    #equipment = relationship("Equipment", secondary=OrderEquipmentJoin, back_populates="order")
    # Обратная связь
    #order = relationship("Equipment", back_populates="purchase_requests")

    order_items = relationship("OrderItem", back_populates="order")

    # Внешний ключ на Customer
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)

    # Внешний ключ на Manager
    manager_id = Column(Integer, ForeignKey("manager.id"), nullable=False)

    manager = relationship("Manager", back_populates="order")
    customer = relationship("Customer", back_populates="order")


    def __init__(self, manager_id: int, customer_id: int):
        self.manager_id = manager_id
        self.customer_id = customer_id
        self.status = 'new'
