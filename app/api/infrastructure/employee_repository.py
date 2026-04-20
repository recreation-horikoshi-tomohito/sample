from app.api.domain.employee import Employee
from app.api.infrastructure.database import get_db


def find_active_employees(app):
    db = get_db(app)
    rows = db.execute(
        "SELECT id, name, role, position, department, age, hire_date"
        " FROM employees WHERE status = '在籍中'"
    ).fetchall()
    return [Employee(**dict(row)) for row in rows]


def find_active_employee_by_id(app, employee_id):
    db = get_db(app)
    row = db.execute(
        "SELECT id, name, role, position, department, age, hire_date"
        " FROM employees WHERE id = ? AND status = '在籍中'",
        (employee_id,)
    ).fetchone()
    if row is None:
        return None
    return Employee(**dict(row))
