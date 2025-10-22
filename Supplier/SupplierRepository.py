from typing import List, Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status

from Equipments.EquipmentDto import EquipmentDtoCreate
from Equipments.EquipmentModel import Equipment
from Orders.OrderModel import Order
from Supplier.SupplierMapper import SupplierMapper
from Supplier.SupplierModel import Supplier


class SupplierRepository:
    __path: str
    __engine: Engine

    def __init__(self, db):
        self.db = db


    def get_supplier_by_id(self, supplier_id: int):  #"-> Optional[MediaSet]:
        supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Производитель с id={supplier_id} не найден"
            )
        return SupplierMapper.to_dto(supplier)

    def get_all_pg(self, skip: int = 0, limit: int = 10):
        # всего записей
        total = self.db.query(Supplier).count()

        # данные с учетом пагинации
        suppliers = (
            self.db.query(Supplier)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [SupplierMapper.to_dto(x) for x in suppliers]



    # def get_all(self) -> List[Order]:
    #     return self.db.query(Order).all()

    # def get_all_with_media(self) -> List[MediaSetResponseWithMedia] | None:
    #    # mediaset = self.db.query(MediaSet).filter(MediaSet.id == mediaset_id).first()
    #     mediasets = self.db.query(MediaSet).all()
    #     if not mediasets:
    #         return None
    #     return [MediaSetResponseWithMedia(
    #         id=ms.id,
    #         name=ms.name,
    #         photos=[
    #             MediaResponseWithUrl(
    #                 id=media.id,
    #                 name=media.name,
    #                 thumbUrl=f"http://localhost:8000/api/media/{media.id}"
    #             )
    #             for media in ms.media
    #         ]
    #     )for ms in mediasets]

    # def get_all_mediaset_with_media(self) -> List[MediaSetResponseWithMedia] | None:
    #     mediasets = self.db.query(MediaSet).all()
    #     if not mediasets:
    #         return None
    #     []
    #     MediaSetResponseWithMedia(
    #         id=mediaset.id,
    #         name=mediaset.name,
    #         medias=[
    #             MediaSetResponseWithUrl(
    #                 id=m.id,
    #                 name=m.name,
    #                 url=f"/api/media/{m.id}"
    #             )
    #             for m in mediaset.media
    #         ]
    #     )
    #     return

    # def update_mediaset(self, mediaset_id: int, update_model: UpdateMediaSetModel) -> Optional[MediaSet]:
    #     db: Session = self.SessionLocal()
    #     mediaset = db.query(MediaSet).filter(MediaSet.id == mediaset_id).first()
    #     if not mediaset:
    #         return None
    #     if update_model.text is not None:
    #         mediaset.text = update_model.text
    #     db.commit()
    #     db.refresh(mediaset)
    #     return mediaset

    # def delete_mediaset(self, mediaset_id: int) -> bool:
    #     #SessionLocal = sessionmaker(autoflush=False, bind=self.__engine)
    #     #db = SessionLocal()
    #     mediaset = self.db.query(MediaSet).filter(MediaSet.id == mediaset_id).first()
    #     if not mediaset:
    #         return False
    #     self.db.delete(mediaset)
    #     self.db.commit()
    #     return True

    # def delete_media_from_mediaset(self, media_set:MediaSet, media:Media):
    #     try:
    #         media_set.media.remove(media)
    #         self.db.commit()
    #         return True
    #     except Exception as e:
    #         self.db.rollback()
    #         raise ValueError(f"Ошибка при удалении {media.name} из набора {media_set.name}")
    #         return False

    # def append_media(self, mediaSet:MediaSet, media:Media):
    #     try:
    #         mediaSet.media.append(media)
    #         self.db.commit()
    #         self.db.refresh(mediaSet)
    #     except Exception as e:
    #         self.db.rollback()
    #         raise ValueError(f"Ошибка! Файл {media.name} уже есть в наборе {mediaSet.name}")

    # def get_all(self) -> List[MediaSet]:
    #     db: Session = self.SessionLocal()
    #     return db.query(MediaSet).all()
    #

