from app.api.infrastructure.employee_repository import find_active_employees


def get_employees(app):
    employees = find_active_employees(app)
    return [e.to_dict() for e in employees]
