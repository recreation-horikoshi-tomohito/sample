from app.api.infrastructure.models.employee_model import EmployeeModel
from app.api.infrastructure.repository.employee_repository import (
    SQLiteEmployeeRepository,
)
from app.api.core.usecase.employee.find_employee_detail import FindEmployeeDetailUseCase


def seed_one(db_session, employee):
    model = EmployeeModel(**employee)
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model.id


# --- US3: FindEmployeeDetailUseCase インテグレーションテスト ---


def test_在籍中社員の詳細が取得できる(app, db_session):
    eid = seed_one(
        db_session,
        {
            "name": "山田太郎",
            "role": "エンジニア",
            "position": "主任",
            "department": "開発部",
            "age": 32,
            "hire_date": "2021-04-01",
            "status": "在籍中",
        },
    )
    with app.app_context():
        result = FindEmployeeDetailUseCase(SQLiteEmployeeRepository()).execute(eid)
    assert result is not None
    assert result.name == "山田太郎"
    assert result.years_of_service >= 0


def test_存在しないIDはNoneを返す(app, db_session):
    with app.app_context():
        result = FindEmployeeDetailUseCase(SQLiteEmployeeRepository()).execute(9999)
    assert result is None


def test_退職済み社員はNoneを返す(app, db_session):
    eid = seed_one(
        db_session,
        {
            "name": "退職者",
            "role": "エンジニア",
            "position": "一般",
            "department": "開発部",
            "age": 35,
            "hire_date": "2020-04-01",
            "status": "退職済",
        },
    )
    with app.app_context():
        result = FindEmployeeDetailUseCase(SQLiteEmployeeRepository()).execute(eid)
    assert result is None
