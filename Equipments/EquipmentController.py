import json
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, UploadFile, File, Query, Depends, Body, HTTPException
from fastapi.responses import Response


from Equipments.EquipmentDto import EquipmentDtoCreate, EquipmentUpdate
from Equipments.EquipmentRepository import EquipmentRepository


class EquipmentController:
    def __init__(self, repo):
        self.router = APIRouter(prefix="/api/equipment")
        self.repo: EquipmentRepository = repo
        self.router.add_api_route(
            "/create", self.create_equipment, methods=["POST"]
        )
        self.router.add_api_route(
            "/{equipment_id}", self.get_equipment_by_id, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "", self.get_equipment_with_pg, methods=["GET"])

        self.router.add_api_route(
            "/{equipment_id}", self.update_equipment, methods=["PATCH"])

        self.router.add_api_route(
            "/{equipment_id}", self.delete_equipment, methods=["DELETE"])

    async def create_equipment(self, equipment: EquipmentDtoCreate):
        createdEquipment = self.repo.create_equipment(equipment)
        return createdEquipment

    def get_equipment_with_pg(self,
                              skip: int = Query(0, ge=0),
                              limit: int = Query(10, ge=1, le=100)):
        return self.repo.get_all_pg(skip=skip, limit=limit)

    def get_equipment_by_id(self,
                        equipment_id: int,
                        ):
        equipment = self.repo.get_equipment_by_id(equipment_id)
        return equipment

    def update_equipment(self,
            equipment_id: int,
            eq_update: EquipmentUpdate = Body(...)
    ):
        updated = self.repo.update_equipment(equipment_id, eq_update)
        if not updated:
            raise HTTPException(status_code=404, detail="Оборудование не найдено")
        return updated

    def delete_equipment(self,
                     equipment_id: int):
            return self.repo.delete_equipment(equipment_id)
