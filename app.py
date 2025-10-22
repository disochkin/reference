from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import init_db
from Customers.CustomerController import CustomerController
from Customers.CustomerRepository import CustomerRepository
from Equipments.EquipmentController import EquipmentController
from Equipments.EquipmentRepository import EquipmentRepository
from ExceptionHandler import register_exception_handlers
from Managers.ManagerController import ManagerController
from Managers.ManagerRepository import ManagerRepository
from OrderItem.OrderItemRepository import OrderItemRepository
from Supplier.SupplierController import SupplierController
from Supplier.SupplierRepository import SupplierRepository
from database import db
from database import Base, engine
##
from Equipments.EquipmentModel import Equipment
from Orders.OrderModel import Order
from Customers.CustomerModel import Customer
from Managers.ManagerModel import Manager
from Supplier.SupplierModel import Supplier
from OrderItem.OrderItemModel import OrderItem

from Orders.OrderController import OrderController
from Orders.OrderRepository import OrderRepository
from load_data_from_csv import load_csv_to_db

Base.metadata.create_all(bind=engine)

app = FastAPI()
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

equipment_repo = EquipmentRepository(db)
equipment_controller = EquipmentController(equipment_repo)
app.include_router(equipment_controller.router)

repoOrder = OrderRepository(db)
repoOrderItem = OrderItemRepository(db)
#repoOrder, repoItems, repoEquipment
order_controller = OrderController(repoOrder, repoOrderItem, equipment_repo)
app.include_router(order_controller.router)

supplier_repo = SupplierRepository(db)
supplier_controller = SupplierController(supplier_repo)
app.include_router(supplier_controller.router)

customer_repo = CustomerRepository(db)
customer_controller = CustomerController(customer_repo)
app.include_router(customer_controller.router)

manager_repo = ManagerRepository(db)
manager_controller = ManagerController(manager_repo)
app.include_router(manager_controller.router)

init_db.init(db)
# load_csv_to_db("import_data/managers.csv", Manager, db)
# load_csv_to_db("import_data/suppliers.csv", Supplier, db)
# load_csv_to_db("import_data/equipment.csv", Equipment, db)
# load_csv_to_db("import_data/customers.csv", Customer, db)
