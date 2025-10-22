# app/mappers/equipment_mapper.py
from Supplier.SupplierDto import SupplierDtoFormResponse
from Supplier.SupplierModel import Supplier


class SupplierMapper:

    # @staticmethod
    # def to_model(dto: EquipmentCreate) -> Equipment:
    #     """Pydantic → ORM"""
    #     return Equipment(name=dto.name, price=dto.price)

    @staticmethod
    def to_dto(model: Supplier) -> SupplierDtoFormResponse:
        """ORM → Pydantic"""
        return SupplierDtoFormResponse.model_validate(model)