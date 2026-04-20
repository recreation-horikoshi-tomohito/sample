from app.api.infrastructure.database import get_db


def seed(app, employees):
    with app.app_context():
        db = get_db(app)
        db.executemany(
            "INSERT INTO employees (name, role, position, department, age, hire_date, status)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (e["name"], e["role"], e["position"], e["department"],
                 e["age"], e["hire_date"], e["status"])
                for e in employees
            ],
        )
        db.commit()


# --- US1: 在籍中の社員一覧の取得 ---

def test_在籍中の社員のみ返される(client, app):
    seed(app, [
        {"name": "山田太郎", "role": "エンジニア", "position": "主任",
         "department": "開発部", "age": 32, "hire_date": "2021-04-01", "status": "在籍中"},
        {"name": "佐藤花子", "role": "デザイナー", "position": "一般",
         "department": "デザイン部", "age": 27, "hire_date": "2024-10-01", "status": "退職済"},
    ])
    response = client.get("/api/employees")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "山田太郎"


def test_退職済社員は含まれない(client, app):
    seed(app, [
        {"name": "田中次郎", "role": "マネージャー", "position": "課長",
         "department": "営業部", "age": 40, "hire_date": "2015-04-01", "status": "退職済"},
    ])
    response = client.get("/api/employees")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_在籍中の社員が0名のとき空配列を返す(client, app):
    response = client.get("/api/employees")
    assert response.status_code == 200
    assert response.get_json() == []


def test_レスポンスに必要なフィールドが含まれる(client, app):
    seed(app, [
        {"name": "鈴木三郎", "role": "エンジニア", "position": "一般",
         "department": "開発部", "age": 25, "hire_date": "2025-04-01", "status": "在籍中"},
    ])
    response = client.get("/api/employees")
    data = response.get_json()
    employee = data[0]
    assert "id" in employee
    assert "name" in employee
    assert "role" in employee
    assert "position" in employee
    assert "department" in employee
    assert "age" in employee
    assert "hire_date" in employee
    assert "years_of_service" in employee
    assert "status" not in employee  # statusはレスポンスに含まない


# --- US2: 勤続年数の自動計算 ---

def test_勤続年数が正しく計算される(client, app):
    seed(app, [
        {"name": "古参社員", "role": "エンジニア", "position": "部長",
         "department": "開発部", "age": 45, "hire_date": "2021-04-20", "status": "在籍中"},
    ])
    response = client.get("/api/employees")
    data = response.get_json()
    # 2026-04-20 時点で2021-04-20入社 → 5年
    assert data[0]["years_of_service"] == 5


def test_今年入社の社員は勤続0年(client, app):
    seed(app, [
        {"name": "新入社員", "role": "エンジニア", "position": "一般",
         "department": "開発部", "age": 23, "hire_date": "2026-04-01", "status": "在籍中"},
    ])
    response = client.get("/api/employees")
    data = response.get_json()
    assert data[0]["years_of_service"] == 0


def test_勤続年数は端数切り捨て(client, app):
    seed(app, [
        {"name": "中堅社員", "role": "エンジニア", "position": "主任",
         "department": "開発部", "age": 30, "hire_date": "2024-10-01", "status": "在籍中"},
    ])
    response = client.get("/api/employees")
    data = response.get_json()
    # 2026-04-20 時点で2024-10-01入社 → 1年と約7ヶ月 → 切り捨て1年
    assert data[0]["years_of_service"] == 1
