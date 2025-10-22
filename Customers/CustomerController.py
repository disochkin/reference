import json
from http.client import HTTPException

from fastapi import APIRouter, UploadFile, File, Query, Depends, Body
from fastapi.responses import Response

from Customers.CustomerRepository import CustomerRepository


class CustomerController:
    def __init__(self, repo):
        self.router = APIRouter(prefix="/api/customer")
        self.repo: CustomerRepository = repo

        self.router.add_api_route(
            "/{customer_id}", self.get_customer_by_id, methods=["GET"], response_model=None)

        self.router.add_api_route(
            "", self.get_all, methods=["GET"])


    def get_all(self):
        return self.repo.get_all()

    def get_customer_by_id(self,
                        customer_id: int):
        customer = self.repo.get_customer_by_id(customer_id)
        return customer