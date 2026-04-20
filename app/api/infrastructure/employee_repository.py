from app.api.domain.employee import Employee
from app.api.infrastructure.database import get_db


def find_active_employees(app):
    db = get_db(app)
    rows = db.execute(
        "SELECT id, name, role, position, department, age, hire_date"
        " FROM employees WHERE status = '在籍中'"
    ).fetchall()
    return [Employee(**dict(row)) for row in rows]
