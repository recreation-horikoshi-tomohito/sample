from flask import Blueprint, jsonify
from injector import inject

from app.usecase.customers.list import IListCustomersUseCase, ListCustomersInput

bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/", methods=["GET"])
@inject
def list_customers(use_case: IListCustomersUseCase):
    output = use_case.execute(ListCustomersInput())
    return jsonify(
        [
            {"id": c.id, "name": c.name, "email": c.email}
            for c in output.customers
        ]
    )
