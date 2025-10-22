# app/mappers/equipment_mapper.py
from Equipments.EquipmentDto import EquipmentDtoResponse
from Equipments.EquipmentModel import Equipment


class EquipmentMapper:

    # @staticmethod
    # def to_model(dto: EquipmentCreate) -> Equipment:
    #     """Pydantic → ORM"""
    #     return Equipment(name=dto.name, price=dto.price)

    @staticmethod
    def to_dto_response_table(model: Equipment) -> EquipmentDtoResponse:
        """ORM → Pydantic"""
        return EquipmentDtoResponse.model_validate(model)