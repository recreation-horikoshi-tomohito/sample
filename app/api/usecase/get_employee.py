from app.api.infrastructure.employee_repository import find_active_employee_by_id


def get_employee(app, employee_id):
    employee = find_active_employee_by_id(app, employee_id)
    if employee is None:
        return None
    return employee.to_dict()
