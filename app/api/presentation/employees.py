import re
from dataclasses import asdict
from flask import Blueprint, jsonify, request, current_app
from app.api.core.usecase.employee import (
    IFindEmployeeListUseCase,
    IFindEmployeeDetailUseCase,
    ICreateEmployeeUseCase,
)
from app.api.core.domain.employee import EmployeeInput

employees_bp = Blueprint("employees", __name__)

_REQUIRED_FIELDS = ["name", "role", "position", "department", "age", "hire_date"]
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


@employees_bp.route("/api/employees", methods=["POST"])
def create_employee():
    body = request.get_json(silent=True) or {}
    for field in _REQUIRED_FIELDS:
        if field not in body:
            return jsonify({"error": f"必須フィールドが不足しています: {field}"}), 400
    if not isinstance(body["age"], int) or body["age"] < 0:
        return jsonify({"error": "age は0以上の整数で指定してください"}), 400
    if not body["name"]:
        return jsonify({"error": "name は空文字にできません"}), 400
    if not _DATE_PATTERN.match(str(body["hire_date"])):
        return jsonify({"error": "hire_date は YYYY-MM-DD 形式で指定してください"}), 400
    try:
        usecase = current_app.injector.get(ICreateEmployeeUseCase)
        result = usecase.execute(
            EmployeeInput(
                name=body["name"],
                role=body["role"],
                position=body["position"],
                department=body["department"],
                age=body["age"],
                hire_date=body["hire_date"],
            )
        )
        return jsonify(asdict(result)), 201
    except Exception:
        return jsonify({"error": "サーバーエラーが発生しました"}), 500
