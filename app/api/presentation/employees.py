from flask import Blueprint, jsonify, current_app
from app.api.usecase.get_employees import get_employees

employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/api/employees")
def list_employees():
    return jsonify(get_employees(current_app._get_current_object()))
