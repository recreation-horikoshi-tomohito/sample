from injector import inject
from app.api.core.domain.employee import EmployeeOutput
from app.api.core.domain.repository.employee_repository import IEmployeeRepository
from app.api.core.usecase.employee import IFindEmployeeListUseCase


class FindEmployeeListUseCase(IFindEmployeeListUseCase):
    """
    社員一覧取得ユースケースの具体実装。
    IEmployeeRepositoryから在籍中の社員一覧を取得し、EmployeeOutputのリストとして返す。
    DIによりIEmployeeRepositoryが注入される。
    """
    @inject
    def __init__(self, repo: IEmployeeRepository):
        self.repo = repo

    def execute(self) -> list[EmployeeOutput]:
        return [
            EmployeeOutput(
                id=e.id, name=e.name, role=e.role,
                position=e.position, department=e.department,
                age=e.age, hire_date=e.hire_date,
                years_of_service=e.years_of_service,
            )
            for e in self.repo.find_all()
        ]
