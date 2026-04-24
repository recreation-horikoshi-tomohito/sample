from app.api.infrastructure.repository.employee_repository import (
    SQLiteEmployeeRepository,
)
from app.api.infrastructure.models.employee_model import EmployeeModel


def seed(db_session, employees):
    for e in employees:
        db_session.add(EmployeeModel(**e))
    db_session.commit()


# --- US1: 正常系テスト ---


def test_find_all_在籍中のみ返す(app, db_session):
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
            {
                "name": "佐藤花子",
                "role": "デザイナー",
                "position": "一般",
                "department": "デザイン部",
                "age": 27,
                "hire_date": "2024-10-01",
                "status": "退職済",
            },
        ],
    )
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        result = repo.find_all()
    assert len(result) == 1
    assert result[0].name == "山田太郎"


def test_find_all_空リストを返す(app, db_session):
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        result = repo.find_all()
    assert result == []


def test_find_all_全フィールドが含まれる(app, db_session):
    seed(
        db_session,
        [
            {
                "name": "鈴木三郎",
                "role": "エンジニア",
                "position": "一般",
                "department": "開発部",
                "age": 25,
                "hire_date": "2025-04-01",
                "status": "在籍中",
            },
        ],
    )
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        result = repo.find_all()
    e = result[0]
    assert e.id is not None
    assert e.name == "鈴木三郎"
    assert e.role == "エンジニア"
    assert e.position == "一般"
    assert e.department == "開発部"
    assert e.age == 25
    assert e.hire_date == "2025-04-01"


def test_find_by_id_在籍中社員を返す(app, db_session):
    seed(
        db_session,
        [
            {
                "name": "田中次郎",
                "role": "マネージャー",
                "position": "課長",
                "department": "営業部",
                "age": 40,
                "hire_date": "2015-04-01",
                "status": "在籍中",
            },
        ],
    )
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        all_employees = repo.find_all()
        eid = all_employees[0].id
        result = repo.find_by_id(eid)
    assert result is not None
    assert result.name == "田中次郎"


# --- US2: 異常系テスト ---


def test_find_by_id_退職済は返さない(app, db_session):
    seed(
        db_session,
        [
            {
                "name": "退職者",
                "role": "エンジニア",
                "position": "一般",
                "department": "開発部",
                "age": 35,
                "hire_date": "2020-04-01",
                "status": "退職済",
            },
        ],
    )
    with app.app_context():
        row = db_session.query(EmployeeModel).filter_by(name="退職者").first()
        eid = row.id
        repo = SQLiteEmployeeRepository()
        result = repo.find_by_id(eid)
    assert result is None


def test_find_by_id_存在しないIDはNone(app, db_session):
    with app.app_context():
        repo = SQLiteEmployeeRepository()
        result = repo.find_by_id(9999)
    assert result is None
