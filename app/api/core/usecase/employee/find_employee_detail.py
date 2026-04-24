from injector import inject
from app.api.core.domain.employee import EmployeeOutput
from app.api.core.domain.repository.employee_repository import IEmployeeRepository
from app.api.core.usecase.employee import IFindEmployeeDetailUseCase


class FindEmployeeDetailUseCase(IFindEmployeeDetailUseCase):
    """
    社員詳細取得ユースケースの具体実装。
    指定IDの在籍中社員をIEmployeeRepositoryから取得し、EmployeeOutputとして返す。
    社員が存在しない場合はNoneを返す。DIによりIEmployeeRepositoryが注入される。
    """

    @inject
    def __init__(self, repo: IEmployeeRepository):
        self.repo = repo

    def execute(self, employee_id) -> EmployeeOutput | None:
        e = self.repo.find_by_id(employee_id)
        if e is None:
            return None
        return EmployeeOutput(
            id=e.id,
            name=e.name,
            role=e.role,
            position=e.position,
            department=e.department,
            age=e.age,
            hire_date=e.hire_date,
            years_of_service=e.years_of_service,
        )
