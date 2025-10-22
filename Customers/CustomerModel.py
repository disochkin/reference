
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, func
from sqlalchemy.orm import relationship

from database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    baseDiscount = Column(Integer, default=0)

    # Связь: один покупатель — много заявок
    order = relationship("Order", back_populates="customer")


