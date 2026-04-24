from injector import inject
from app.api.core.domain.employee import EmployeeCreateOutput
from app.api.core.domain.repository.employee_repository import IEmployeeRepository
from app.api.core.usecase.employee import ICreateEmployeeUseCase


class CreateEmployeeUseCase(ICreateEmployeeUseCase):
    """
    社員登録ユースケースの具体実装。
    IEmployeeRepository.save()で社員を永続化し、EmployeeCreateOutputとして返す。
    """

    @inject
    def __init__(self, repo: IEmployeeRepository):
        self.repo = repo

    def execute(self, input) -> EmployeeCreateOutput:
        employee = self.repo.save(input)
        return EmployeeCreateOutput(
            id=employee.id,
            name=employee.name,
            role=employee.role,
            position=employee.position,
            department=employee.department,
            age=employee.age,
            hire_date=employee.hire_date,
            status="在籍中",
        )
