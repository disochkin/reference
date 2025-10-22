import json
from http.client import HTTPException

from fastapi import APIRouter, UploadFile, File, Query, Depends, Body
from fastapi.responses import Response

from Customers.CustomerRepository import CustomerRepository
from Managers.ManagerRepository import ManagerRepository


class ManagerController:
    def __init__(self, repo):
        self.router = APIRouter(prefix="/api/manager")
        self.repo: ManagerRepository = repo

        self.router.add_api_route(
            "/{manager_id}", self.get_manager_by_id, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "", self.get_all, methods=["GET"])


    def get_all(self):
        return self.repo.get_all()

    def get_manager_by_id(self,
                        manager_id: int):
        manager = self.repo.get_manager_by_id(manager_id)
        return manager