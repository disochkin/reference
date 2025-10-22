# app/mappers/equipment_mapper.py
from Customers.CustomerDto import CustomerDtoShort
from Customers.CustomerModel import Customer
from Equipments.EquipmentDto import EquipmentDtoResponse
from Equipments.EquipmentModel import Equipment


class CustomerMapper:

    # @staticmethod
    # def to_model(dto: EquipmentCreate) -> Equipment:
    #     """Pydantic → ORM"""
    #     return Equipment(name=dto.name, price=dto.price)

    @staticmethod
    def to_dto_response_table(model: Customer) -> CustomerDtoShort:
        """ORM → Pydantic"""
        return CustomerDtoShort.model_validate(model)