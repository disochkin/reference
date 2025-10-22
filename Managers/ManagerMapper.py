# app/mappers/equipment_mapper.py
from Customers.CustomerDto import CustomerDtoShort
from Customers.CustomerModel import Customer
from Equipments.EquipmentDto import EquipmentDtoResponse
from Equipments.EquipmentModel import Equipment
from Managers.ManagerDto import ManagerDtoShort
from Managers.ManagerModel import Manager


class ManagerMapper:

    # @staticmethod
    # def to_model(dto: EquipmentCreate) -> Equipment:
    #     """Pydantic → ORM"""
    #     return Equipment(name=dto.name, price=dto.price)

    @staticmethod
    def to_dto_response_table(model: Manager) -> ManagerDtoShort:
        """ORM → Pydantic"""
        return ManagerDtoShort.model_validate(model)