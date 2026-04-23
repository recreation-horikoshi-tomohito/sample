from flask import current_app
from app.api.core.domain.employee.employee import Employee
from app.api.core.domain.repository.employee_repository import IEmployeeRepository
from app.api.infrastructure.database import get_session
from app.api.infrastructure.models.employee_model import EmployeeModel


class SQLiteEmployeeRepository(IEmployeeRepository):
    """
    IEmployeeRepositoryのSQLite実装。
    infrastructure層に属し、SQLAlchemy ORM を通じてデータベースへのアクセスを担う。
    在籍中の社員のみを対象としたクエリを実行し、Employeeエンティティとして返す。
    """

    def find_all(self) -> list[Employee]:
        session = get_session(current_app._get_current_object())
        rows = session.query(EmployeeModel).filter_by(status="在籍中").all()
        return [self._to_entity(row) for row in rows]

    def find_by_id(self, employee_id: int) -> Employee | None:
        session = get_session(current_app._get_current_object())
        row = session.query(EmployeeModel).filter_by(id=employee_id, status="在籍中").first()
        if row is None:
            return None
        return self._to_entity(row)

    def _to_entity(self, model) -> Employee:
        return Employee(
            id=model.id, name=model.name, role=model.role,
            position=model.position, department=model.department,
            age=model.age, hire_date=model.hire_date,
        )
