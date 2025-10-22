import json
from http.client import HTTPException

from fastapi import APIRouter, UploadFile, File, Query, Depends
from fastapi.responses import Response


from Equipments.EquipmentDto import EquipmentDtoCreate
from Orders.OrderRepository import OrderRepository
from Supplier.SupplierRepository import SupplierRepository


class SupplierController:
    def __init__(self, repo):
        self.router = APIRouter(prefix="/api/supplier")
        self.repo:SupplierRepository = repo
        self.router.add_api_route(
            "/{supplier_id}", self.get_supplier_by_id, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "", self.get_all_pg, methods=["GET"])

    def get_supplier_by_id(self,
                        supplier_id: int,
                        ):
        supplier = self.repo.get_supplier_by_id(supplier_id)
        return supplier

    def get_all_pg(self,
                              skip: int = Query(0, ge=0),
                              limit: int = Query(10, ge=1, le=100)):
        return self.repo.get_all_pg(skip=skip, limit=limit)



    # def delete_media(self,
    #                  media_id: int,
    #                  current_user=Depends(get_current_user),):
    #     success = self.repo.delete_media(media_id)
    #     if not success:
    #         raise HTTPException(status_code=404, detail="MediaSet not found")
    #     return {"deleted": True}
