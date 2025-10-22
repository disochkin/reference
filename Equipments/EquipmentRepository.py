import sqlite3
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import HTTPException, status

from Equipments.EquipmentDto import EquipmentDtoCreate, EquipmentUpdate
from Equipments.EquipmentMapper import EquipmentMapper
from Equipments.EquipmentModel import Equipment


class EquipmentRepository:
    __path: str
    __engine: Engine

    def __init__(self, db):
        self.db = db

    def create_equipment(self, equipment: EquipmentDtoCreate) -> Equipment:
        equipment = Equipment(equipment.name, equipment.price, equipment.supplier_id)
        self.db.add(equipment)
        self.db.commit()
        self.db.refresh(equipment)  # чтобы подтянуть id из БД
        return equipment


    def get_equipment_by_id(self, equipment_id: int):  #"-> Optional[MediaSet]:
        equipment = self.db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Оборудование с id={equipment_id} не найдено"
            )
        return equipment

    def get_all_pg(self, skip: int = 0, limit: int = 10):
        # всего записей
        total = self.db.query(Equipment).count()

        # данные с учетом пагинации
        equipment = (
            self.db.query(Equipment)
            .options(joinedload(Equipment.supplier))  # подгружаем поставщика
            .offset(skip)
            .limit(limit)
            .all()
        )
        return {
            "total": total,
            "items": [EquipmentMapper.to_dto_response_table(x) for x in equipment]
        }

    def get_all(self) -> List[Equipment]:
        return self.db.query(Equipment).all()

    def update_equipment(self, equipment_id: int, equipmentUpdate: EquipmentUpdate):
        equipment = self.get_equipment_by_id(equipment_id)
        if not equipment:
            return None

        update_data = equipmentUpdate.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(equipment, key, value)

        self.db.commit()
        self.db.refresh(equipment)
        return equipment

    def delete_equipment(self, equipment_id: int) -> bool:
        equipment = self.db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Оборудование с id={equipment_id} не найдено")
        try:
            self.db.delete(equipment)
            self.db.commit()
            return equipment
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Невозможно удалить: есть связанные записи."
            )
        except Exception as e:
            self.db.rollback()
            raise ValueError("Неизвестная ошибка: ", str(e))
