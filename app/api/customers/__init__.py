from flask import Blueprint, jsonify, request
from injector import inject
from app.usecase.customers import IListCustomersUseCase, ListCustomersInput

bp = Blueprint("customers", __name__)


@bp.get("/customers")
@inject
def list_customers(use_case: IListCustomersUseCase):
    email = request.args.get("email")
    result = use_case.execute(ListCustomersInput(email=email))
    return jsonify([{"id": c.id, "name": c.name, "email": c.email} for c in result.customer_list])
