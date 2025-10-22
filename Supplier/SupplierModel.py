
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, func
from sqlalchemy.orm import relationship

from database import Base


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Связь: один поставщик — много оборудования
    equipment = relationship("Equipment", back_populates="supplier")


