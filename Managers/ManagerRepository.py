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
from Managers.ManagerDto import ManagerDtoShort
from Managers.ManagerMapper import ManagerMapper
from Managers.ManagerModel import Manager


class ManagerRepository:
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


    def get_manager_by_id(self, manager_id: int):  #"-> Optional[MediaSet]:
        manager = self.db.query(Manager).filter(Manager.id == manager_id).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Менеджер с id={manager_id} не найден"
            )
        return manager

    def get_all(self) -> List[ManagerDtoShort]:
        managers = self.db.query(Manager).all()
        return [ManagerMapper.to_dto_response_table(x) for x in managers]



