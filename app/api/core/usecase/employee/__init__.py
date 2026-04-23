from abc import ABC, abstractmethod
from app.api.core.domain.employee import EmployeeOutput


class IFindEmployeeListUseCase(ABC):
    """
    社員一覧取得ユースケースのインターフェース。
    presentation層がこのインターフェースに依存することで、具体実装と分離する。
    """
    @abstractmethod
    def execute(self) -> list[EmployeeOutput]:
        raise NotImplementedError


class IFindEmployeeDetailUseCase(ABC):
    """
    社員詳細取得ユースケースのインターフェース。
    presentation層がこのインターフェースに依存することで、具体実装と分離する。
    """
    @abstractmethod
    def execute(self, employee_id) -> EmployeeOutput | None:
        raise NotImplementedError
