from sqlite3 import IntegrityError
from typing import List, Optional

from sqlalchemy import create_engine, Engine, func
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import HTTPException, status

import Managers
from Equipments.EquipmentDto import EquipmentDtoCreate
from Equipments.EquipmentModel import Equipment
from Managers.ManagerModel import Manager
from OrderItem.OrderItemModel import OrderItem
from Orders.OrderDto import OrderDtoCreate, OrderDtoResponse, OrderDtoResponseFull
from Orders.OrderMapper import OrderMapper
from Orders.OrderModel import Order


class OrderRepository:
    __path: str
    __engine: Engine

    def __init__(self, db):
        self.db = db

    def create_order(self, order: OrderDtoCreate) -> Order:
        order: Order = Order(manager_id=order.manager_id, customer_id=order.customer_id)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)  # чтобы подтянуть id из БД
        return order


    def get_order_by_id(self, order_id: int):  #"-> Optional[MediaSet]:
        order: OrderDtoResponse = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заявка с id={order_id} не найдена"
            )
        return order

    #

    def delete_order(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Заявка с id={order_id} не найдена")
        try:
            self.db.delete(order)
            self.db.commit()
            return order
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Невозможно удалить: есть связанные записи."
            )
        except Exception as e:
            self.db.rollback()
            raise ValueError("Неизвестная ошибка: ", str(e))



    def get_order_by_id_with_items(self, order_id: int):  #"-> Optional[MediaSet]:
        order: Order = (self.db.query(Order)
                                       .options(joinedload(Order.manager))
                                       .options(joinedload(Order.customer))
                                       .options(joinedload(Order.order_items))
                                       .filter(Order.id == order_id).first())
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заявка с id={order_id} не найдена"
            )
       # position_sum = sum(item.price_per_unit * item.quantity for item in order.order_items)
        return OrderMapper.to_dto_response_tableEdit(order)

    def get_order_with_pg_table(self, skip: int = 0, limit: int = 10):
        # всего записей
        total = self.db.query(Order).count()
        # данные с учетом пагинации
        orders = (
            self.db.query(Order)
            .options(joinedload(Order.manager))  # подгружаем менеджера
            .options(joinedload(Order.customer))
            .options(joinedload(Order.order_items))  # <-- обязательно подгрузи позиции
            .offset(skip)
            .limit(limit)
            .all()
        )
        result = []
        for order in orders:
            total_sum = sum(item.price_per_unit * item.quantity for item in order.order_items)
            dto = OrderMapper.to_dto_response_table(order)
            dto.total_sum = total_sum
            result.append(dto)
        return {"total": total, "items": result}

    def get_all(self) -> List[Order]:
        return self.db.query(Order).all()

    # от заказов к позициям
    def get_discount(self, customer_id) -> float:
        total_purchase = (self.db.query(func.sum(OrderItem.quantity * OrderItem.price_per_unit))
                          .select_from(Order)
                          .join(OrderItem, OrderItem.order_id == Order.id)
                          .filter(Order.customer_id == customer_id)
                          .scalar()) or 0
    #Возвращает процент скидки в зависимости от суммы покупок.
        if total_purchase >= 100000:
            return 10.0
        elif total_purchase >= 50000:
            return 7.0
        elif total_purchase >= 20000:
            return 5.0
        elif total_purchase >= 10000:
            return 3.0
        else:
            return 0.0

    # SELECT sum(oi.quantity * oi.price_per_unit ) FROM "order" o
    # JOIN order_items oi
    # ON o.id  = oi.order_id
    # WHERE o.customer_id = 1



