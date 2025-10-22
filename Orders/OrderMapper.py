# app/mappers/equipment_mapper.py
from Equipments.EquipmentDto import EquipmentDtoResponse
from Equipments.EquipmentModel import Equipment
from Orders.OrderDto import OrderDtoResponseTable, OrderDtoResponseFull
from Orders.OrderModel import Order


class OrderMapper:

    # @staticmethod
    # def to_model(dto: EquipmentCreate) -> Equipment:
    #     """Pydantic → ORM"""
    #     return Equipment(name=dto.name, price=dto.price)

    @staticmethod
    def to_dto_response_table(model: Order) -> OrderDtoResponseTable:
        """ORM → Pydantic"""
        return OrderDtoResponseTable.model_validate(model)

    @staticmethod
    def to_dto_response_tableEdit(model: Order) -> OrderDtoResponseFull:
        """ORM → Pydantic"""
        return OrderDtoResponseFull.model_validate(model)