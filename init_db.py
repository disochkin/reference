from Customers.CustomerModel import Customer
from Equipments.EquipmentModel import Equipment
from Managers.ManagerModel import Manager
from Supplier.SupplierModel import Supplier


def init(db):
    managers = [Manager(name="Иванов ИИ", grade="менеждер", phone='8706957', email='sdjlk@ruir.ru'),
                Manager(name="Петров ПП", grade="менеждер", phone='2343244', email='sdfeef@ruir.ru'),
                Manager(name="Сидоров СС", grade="менеждер", phone='4354654', email='fvfbfb@ruir.ru'),
                Manager(name="Смирнов ММ", grade="менеждер", phone='6435345', email='bfdbfr@ruir.ru'),
                Manager(name="Козлов КК", grade="менеждер", phone='1232344', email='vfbbfbk@ruir.ru')]
    db.add_all(managers)
    db.commit()
    db.close()

    suppliers = [Supplier(name="поставщик 1",phone="88049580435",email="ejrerer@jejfoif.ru", country="Россия"),
                 Supplier(name="поставщик 2",phone="55654656565",email="fbgbn@fgfghgh.ru", country="Франция"),
                 Supplier(name="поставщик 3",phone="98058605654",email="ngfng@jfgfdgghd.ru", country="США"),
                 Supplier(name="поставщик 4",phone="65546546546",email="dfnn@nhnn.ru", country="Турция"),
                 Supplier(name="поставщик 5",phone="32325445455",email="eqccwr@dmkdslv.ru", country="Италия")]

    db.add_all(suppliers)
    db.commit()
    db.close()


    equipment = [Equipment(name='Оборудование 1', price=10, supplier_id=1),
                 Equipment(name='Оборудование 2', price=50, supplier_id=1),
                 Equipment(name='Оборудование 3', price=90, supplier_id=3),
                 Equipment(name='Оборудование 4', price=140, supplier_id=5),
                 Equipment(name='Оборудование 5', price=160, supplier_id=5)]
    db.add_all(equipment)
    db.commit()
    db.close()

    customers = [Customer(name="покупатель 1",phone="35435455435",email="ejrerer@jejfoif.ru"),
                 Customer(name="покупатель 2",phone="44565656566",email="ejrerer@jejfoif.ru"),
                 Customer(name="покупатель 3",phone="88049580435",email="ejrerer@jejfoif.ru"),
                 Customer(name="покупатель 4",phone="88049580435",email="ejrerer@jejfoif.ru"),
                 Customer(name="покупатель 5",phone="88049580435",email="ejrerer@jejfoif.ru"),]

    db.add_all(customers)
    db.commit()
    db.close()