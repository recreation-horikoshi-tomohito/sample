from app.api.core.domain.employee import EmployeeInput
from app.api.infrastructure.repository.employee_repository import (
    SQLiteEmployeeRepository,
)
from app.api.core.usecase.employee.create_employee import CreateEmployeeUseCase


# --- CreateEmployeeUseCase インテグレーションテスト ---


def test_社員を登録できる(app, db_session):
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        usecase = CreateEmployeeUseCase(repo)
        input = EmployeeInput(
            name="新田一郎",
            role="エンジニア",
            position="一般",
            department="開発部",
            age=25,
            hire_date="2026-04-01",
        )
        result = usecase.execute(input)
    assert result.id is not None
    assert result.name == "新田一郎"
    assert result.status == "在籍中"


def test_登録結果にyears_of_serviceが含まれない(app, db_session):
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        usecase = CreateEmployeeUseCase(repo)
        input = EmployeeInput(
            name="新田一郎",
            role="エンジニア",
            position="一般",
            department="開発部",
            age=25,
            hire_date="2026-04-01",
        )
        result = usecase.execute(input)
    assert not hasattr(result, "years_of_service")


def test_全フィールドが正確にマッピングされる(app, db_session):
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        usecase = CreateEmployeeUseCase(repo)
        input = EmployeeInput(
            name="佐藤花子",
            role="デザイナー",
            position="リーダー",
            department="デザイン部",
            age=28,
            hire_date="2022-04-01",
        )
        result = usecase.execute(input)
    assert result.name == "佐藤花子"
    assert result.role == "デザイナー"
    assert result.position == "リーダー"
    assert result.department == "デザイン部"
    assert result.age == 28
    assert result.hire_date == "2022-04-01"
    assert result.status == "在籍中"
