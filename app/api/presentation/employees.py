from flask import Blueprint, jsonify, current_app
from app.api.usecase.get_employees import get_employees
from app.api.usecase.get_employee import get_employee

employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/api/employees")
def list_employees():
    return jsonify(get_employees(current_app._get_current_object()))


@employees_bp.route("/api/employees/<int:employee_id>")
def get_employee_by_id(employee_id):
    employee = get_employee(current_app._get_current_object(), employee_id)
    if employee is None:
        return jsonify({"error": "社員が見つかりません"}), 404
    return jsonify(employee)
