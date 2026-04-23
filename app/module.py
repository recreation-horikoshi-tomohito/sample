from injector import Module
from app.api.core.domain.repository.employee_repository import IEmployeeRepository
from app.api.infrastructure.repository.employee_repository import SQLiteEmployeeRepository
from app.api.core.usecase.employee import IFindEmployeeListUseCase, IFindEmployeeDetailUseCase
from app.api.core.usecase.employee.find_employee_list import FindEmployeeListUseCase
from app.api.core.usecase.employee.find_employee_detail import FindEmployeeDetailUseCase


class AppModule(Module):
    """
    DIコンテナの設定モジュール。
    インターフェースと具体実装のバインディングを定義し、
    アプリケーション全体の依存性注入を一元管理する。
    """
    def configure(self, binder):
        binder.bind(IEmployeeRepository, to=SQLiteEmployeeRepository)
        binder.bind(IFindEmployeeListUseCase, to=FindEmployeeListUseCase)
        binder.bind(IFindEmployeeDetailUseCase, to=FindEmployeeDetailUseCase)
