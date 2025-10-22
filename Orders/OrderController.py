from fastapi import APIRouter, Query, HTTPException

from Equipments.EquipmentRepository import EquipmentRepository
from OrderItem.OrderItemDto import OrderItemDtoCreate
from OrderItem.OrderItemModel import OrderItem
from OrderItem.OrderItemRepository import OrderItemRepository
from Orders.OrderDto import OrderDtoCreate
from Orders.OrderRepository import OrderRepository


class OrderController:
    def __init__(self, repoOrder, repoItems, repoEquipment):
        self.router = APIRouter(prefix="/api/order")
        self.repo: OrderRepository = repoOrder
        self.repoItems: OrderItemRepository = repoItems
        self.repoEquipment: EquipmentRepository = repoEquipment
        self.router.add_api_route(
            "/create", self.create_order, methods=["POST"]
        )
        self.router.add_api_route(
            "/{order_id}", self.get_order_by_id, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "/{order_id}/items", self.get_order_by_id_with_items, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "", self.get_order_with_pg, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "/{order_id}", self.get_order_by_id, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "/add_item", self.add_item, methods=["POST"], response_model=None)

        self.router.add_api_route(
            "/discount/{customer_id}", self.get_discount, methods=["GET"])

    async def create_order(self, order: OrderDtoCreate):
        createdOrder = self.repo.create_order(order)
        return createdOrder

    def get_order_by_id(self,
                        order_id: int):
        order = self.repo.get_order_by_id(order_id)
        return order

    def get_order_by_id_with_items(self,
                        order_id: int):
        order = self.repo.get_order_by_id_with_items(order_id)
        print(order)
        return order

    # order_id: int
    # equipment_id: int
    # quantity: int
    #
    # self.order_id = order_id
    # self.equipment_id = equipment_id
    # self.quantity = quantity
    # self.price_per_unit = price_per_unit <- достать из бд
    # self.total_price = quantity * price_per_unit


    def add_item(self,
                 orderItemDtoCreate: OrderItemDtoCreate):
        print(orderItemDtoCreate.model_dump_json())
        order_id = orderItemDtoCreate.order_id
        customer_id = self.repo.get_order_by_id(order_id).customer_id
        discount = self.repo.get_discount(customer_id)
        equipment = self.repoEquipment.get_equipment_by_id(orderItemDtoCreate.equipment_id)
        price = equipment.price * (1-discount/100)
        orderItem: OrderItem = OrderItem(
            order_id=order_id,
            equipment_id = orderItemDtoCreate.equipment_id,
            quantity=orderItemDtoCreate.quantity,
            price_per_unit=price)
        try:
            orderItem = self.repoItems.createOrderItem(orderItem)
            order = self.repo.get_order_by_id(orderItemDtoCreate.order_id)
            return order
        except DuplicateOrderItemError as e:
            raise HTTPException(status_code=400, detail=str(e))


    def get_order_with_pg(self,
                              skip: int = Query(0, ge=0),
                              limit: int = Query(10, ge=1, le=100)):
        return self.repo.get_order_with_pg_table(skip=skip, limit=limit)

    def get_discount(self, customer_id):
        total_purchase = self.repo.total_purchase(customer_id)
        return total_purchase


    # def delete_media(self,
    #                  media_id: int,
    #                  current_user=Depends(get_current_user),):
    #     success = self.repo.delete_media(media_id)
    #     if not success:
    #         raise HTTPException(status_code=404, detail="MediaSet not found")
    #     return {"deleted": True}
