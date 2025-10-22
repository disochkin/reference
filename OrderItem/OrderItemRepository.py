from sqlite3 import IntegrityError
from typing import List, Optional

from sqlalchemy import create_engine, Engine, func
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status

from Equipments.EquipmentDto import EquipmentDtoCreate
from Equipments.EquipmentModel import Equipment
from OrderItem.OrderItemDto import OrderItemDtoCreate
from OrderItem.OrderItemModel import OrderItem
from Orders.OrderDto import OrderDtoCreate, OrderDtoResponse
from Orders.OrderModel import Order


class OrderItemRepository:
    __path: str
    __engine: Engine

    def __init__(self, db):
        self.db = db

    def createOrderItem(self, orderItem: OrderItem) -> Order:
        try:
            self.db.add(orderItem)
            self.db.commit()
            self.db.refresh(orderItem)  # чтобы подтянуть id из БД
            return orderItem
        except Exception as e:
            print(f'order_id: {orderItem.order_id}')
            print(f'equipment_id: {orderItem.equipment_id}')
            print(e)
            self.db.rollback()
            # Проверяем, что именно дублирование
            if "UNIQUE" in str(e.orig) or "unique constraint" in str(e.orig).lower():
                raise DuplicateOrderItemError(
                    f"Оборудование!!! с id={orderItem.equipment_id} уже есть в заявке {orderItem.order_id}"
                )
            else:
                # другие ошибки целостности, например внешние ключи
                raise ValueError(f"Неизвестная ошибка при добавлении позиции: {e}")

        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Ошибка! Оборудование с id={orderItem.equipment_id} "
                             f"уже есть в заявке {orderItem.order_id}")

    def getItemFromOrder(self, order_id):
        orderItem: OrderItem = self.db.query(OrderItem).filter(OrderItem.order_id == order_id)
        return orderItem

    # от позиций к заказам
    # def total_purchase(self, customer_id) -> float:
    #     total_purchase = (self.db.query(func.sum(OrderItem.quantity * OrderItem.price_per_unit))
    #                       .join(Order, Order.id == OrderItem.order_id)
    #                       .filter(Order.customer_id == customer_id)
    #                       .scalar())
    #     return total_purchase or 0

    # SELECT sum(oi.quantity * oi.price_per_unit)
    # FROM order_items oi
    # JOIN "order" o ON
    # o.id = oi.order_id
    # WHERE o.customer_id = 1

