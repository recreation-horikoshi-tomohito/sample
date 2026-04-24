from app.api.infrastructure.models.employee_model import EmployeeModel
from app.api.infrastructure.repository.employee_repository import (
    SQLiteEmployeeRepository,
)
from app.api.core.usecase.employee.find_employee_list import FindEmployeeListUseCase


def seed(db_session, employees):
    for e in employees:
        db_session.add(EmployeeModel(**e))
    db_session.commit()


# --- US3: FindEmployeeListUseCase インテグレーションテスト ---


def test_全フィールドが正確にマッピングされる(app, db_session):
    seed(
        db_session,
        [
            {
                "name": "山田太郎",
                "role": "エンジニア",
                "position": "主任",
                "department": "開発部",
                "age": 32,
                "hire_date": "2021-04-01",
                "status": "在籍中",
            },
        ],
    )
    with app.app_context():
        result = FindEmployeeListUseCase(SQLiteEmployeeRepository()).execute()
    e = result[0]
    assert e.id is not None
    assert e.name == "山田太郎"
    assert e.role == "エンジニア"
    assert e.position == "主任"
    assert e.department == "開発部"
    assert e.age == 32
    assert e.hire_date == "2021-04-01"
    assert e.years_of_service >= 0


def test_勤続年数が正確に計算される(app, db_session):
    seed(
        db_session,
        [
            {
                "name": "古参社員",
                "role": "エンジニア",
                "position": "部長",
                "department": "開発部",
                "age": 45,
                "hire_date": "2021-04-20",
                "status": "在籍中",
            },
        ],
    )
    with app.app_context():
        result = FindEmployeeListUseCase(SQLiteEmployeeRepository()).execute()
    # 2026-04-20 時点で 2021-04-20 入社 → 5年
    assert result[0].years_of_service == 5


def test_在籍中社員のみが返される(app, db_session):
    seed(
        db_session,
        [
            {
                "name": "在籍中社員",
                "role": "エンジニア",
                "position": "一般",
                "department": "開発部",
                "age": 30,
                "hire_date": "2022-04-01",
                "status": "在籍中",
            },
            {
                "name": "退職済社員",
                "role": "デザイナー",
                "position": "一般",
                "department": "デザイン部",
                "age": 35,
                "hire_date": "2018-04-01",
                "status": "退職済",
            },
        ],
    )
    with app.app_context():
        result = FindEmployeeListUseCase(SQLiteEmployeeRepository()).execute()
    assert len(result) == 1
    assert result[0].name == "在籍中社員"
