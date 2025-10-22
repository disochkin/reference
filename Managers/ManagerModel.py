
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, func
from sqlalchemy.orm import relationship

from database import Base

class Manager(Base):
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Связь: один менеждер — много заявок
    order = relationship("Order", back_populates="manager")


