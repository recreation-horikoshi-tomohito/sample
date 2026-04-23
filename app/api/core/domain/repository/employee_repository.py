from abc import ABC, abstractmethod
from app.api.core.domain.employee.employee import Employee


class IEmployeeRepository(ABC):
    """
    社員リポジトリのインターフェース。
    ドメイン層に属し、infrastructure層の具体実装に依存しないよう抽象化する。
    usecase層はこのインターフェースを通じてデータアクセスを行う（依存性逆転の原則）。
    """
    @abstractmethod
    def find_all(self) -> list[Employee]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, employee_id: int) -> Employee | None:
        raise NotImplementedError
