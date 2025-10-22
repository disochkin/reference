from typing import List, Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import HTTPException, status

from Customers.CustomerDto import CustomerDtoShort
from Customers.CustomerMapper import CustomerMapper
from Customers.CustomerModel import Customer
from Equipments.EquipmentDto import EquipmentDtoCreate, EquipmentUpdate
from Equipments.EquipmentMapper import EquipmentMapper
from Equipments.EquipmentModel import Equipment


class CustomerRepository:
    __path: str
    __engine: Engine

    def __init__(self, db):
        self.db = db

    # def create_equipment(self, equipment: EquipmentDtoCreate) -> Equipment:
    #     equipment = Equipment(equipment.name, equipment.price, equipment.supplier_id)
    #     self.db.add(equipment)
    #     self.db.commit()
    #     self.db.refresh(equipment)  # чтобы подтянуть id из БД
    #     return equipment


    def get_customer_by_id(self, customer_id: int):  #"-> Optional[MediaSet]:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Покупатель с id={customer} не найден"
            )
        return customer

    def get_all(self) -> List[CustomerDtoShort]:
        customers = self.db.query(Customer).all()
        return [CustomerMapper.to_dto_response_table(x) for x in customers]



