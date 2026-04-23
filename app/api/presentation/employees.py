from dataclasses import asdict
from flask import Blueprint, jsonify, current_app
from app.api.core.usecase.employee import IFindEmployeeListUseCase, IFindEmployeeDetailUseCase

employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/api/employees")
def list_employees():
    usecase = current_app.injector.get(IFindEmployeeListUseCase)
    return jsonify([asdict(e) for e in usecase.execute()])


@employees_bp.route("/api/employees/<int:employee_id>")
def get_employee_by_id(employee_id):
    usecase = current_app.injector.get(IFindEmployeeDetailUseCase)
    employee = usecase.execute(employee_id)
    if employee is None:
        return jsonify({"error": "社員が見つかりません"}), 404
    return jsonify(asdict(employee))
