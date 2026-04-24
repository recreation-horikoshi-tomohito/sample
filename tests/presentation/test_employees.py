from app.api.infrastructure.models.employee_model import EmployeeModel


def seed(db_session, employees):
    for e in employees:
        db_session.add(EmployeeModel(**e))
    db_session.commit()


def seed_one(db_session, employee):
    model = EmployeeModel(**employee)
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model.id


# --- US1: 在籍中の社員一覧の取得 ---


def test_在籍中の社員のみ返される(client, db_session):
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
    response = client.get("/api/employees")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "山田太郎"


def test_退職済社員は含まれない(client, db_session):
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
                "status": "退職済",
            },
        ],
    )
    response = client.get("/api/employees")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_在籍中の社員が0名のとき空配列を返す(client):
    response = client.get("/api/employees")
    assert response.status_code == 200
    assert response.get_json() == []


def test_レスポンスに必要なフィールドが含まれる(client, db_session):
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


def test_勤続年数が正しく計算される(client, db_session):
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
    response = client.get("/api/employees")
    data = response.get_json()
    # 2026-04-20 時点で2021-04-20入社 → 5年
    assert data[0]["years_of_service"] == 5


def test_今年入社の社員は勤続0年(client, db_session):
    seed(
        db_session,
        [
            {
                "name": "新入社員",
                "role": "エンジニア",
                "position": "一般",
                "department": "開発部",
                "age": 23,
                "hire_date": "2026-04-01",
                "status": "在籍中",
            },
        ],
    )
    response = client.get("/api/employees")
    data = response.get_json()
    assert data[0]["years_of_service"] == 0


def test_勤続年数は端数切り捨て(client, db_session):
    seed(
        db_session,
        [
            {
                "name": "中堅社員",
                "role": "エンジニア",
                "position": "主任",
                "department": "開発部",
                "age": 30,
                "hire_date": "2024-10-01",
                "status": "在籍中",
            },
        ],
    )
    response = client.get("/api/employees")
    data = response.get_json()
    # 2026-04-20 時点で2024-10-01入社 → 1年と約7ヶ月 → 切り捨て1年
    assert data[0]["years_of_service"] == 1


# --- 社員詳細 US1: 社員詳細情報の取得 ---


def test_在籍中社員のIDを指定して詳細情報が取得できる(client, db_session):
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
    response = client.get(f"/api/employees/{eid}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "山田太郎"


def test_詳細レスポンスに必要なフィールドが全て含まれ勤続年数が正確に計算される(
    client, db_session
):
    eid = seed_one(
        db_session,
        {
            "name": "古参社員",
            "role": "エンジニア",
            "position": "部長",
            "department": "開発部",
            "age": 45,
            "hire_date": "2021-04-20",
            "status": "在籍中",
        },
    )
    response = client.get(f"/api/employees/{eid}")
    data = response.get_json()
    assert "id" in data
    assert "name" in data
    assert "role" in data
    assert "position" in data
    assert "department" in data
    assert "age" in data
    assert "hire_date" in data
    assert "years_of_service" in data
    # 2026-04-20 時点で 2021-04-20 入社 → 5年
    assert data["years_of_service"] == 5


def test_詳細レスポンスにstatusフィールドが含まれない(client, db_session):
    eid = seed_one(
        db_session,
        {
            "name": "鈴木三郎",
            "role": "エンジニア",
            "position": "一般",
            "department": "開発部",
            "age": 25,
            "hire_date": "2025-04-01",
            "status": "在籍中",
        },
    )
    response = client.get(f"/api/employees/{eid}")
    data = response.get_json()
    assert "status" not in data


# --- 社員詳細 US2: エラーハンドリング ---


def test_存在しないIDを指定した場合404とエラーメッセージが返る(client):
    response = client.get("/api/employees/9999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "社員が見つかりません"}


def test_退職済み社員のIDを指定した場合404が返る(client, db_session):
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
    response = client.get(f"/api/employees/{eid}")
    assert response.status_code == 404
    assert response.get_json() == {"error": "社員が見つかりません"}


# --- 社員登録 US1: 社員情報を登録する ---


def test_必須フィールドを指定して社員を登録できる(client):
    payload = {
        "name": "新田一郎",
        "role": "エンジニア",
        "position": "一般",
        "department": "開発部",
        "age": 25,
        "hire_date": "2026-04-01",
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "新田一郎"
    assert data["status"] == "在籍中"
    assert "id" in data
    assert "years_of_service" not in data


def test_登録レスポンスに全フィールドが含まれる(client):
    payload = {
        "name": "新田一郎",
        "role": "エンジニア",
        "position": "一般",
        "department": "開発部",
        "age": 25,
        "hire_date": "2026-04-01",
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    for field in [
        "id",
        "name",
        "role",
        "position",
        "department",
        "age",
        "hire_date",
        "status",
    ]:
        assert field in data


def test_登録後にGET一覧に含まれる(client):
    payload = {
        "name": "新田一郎",
        "role": "エンジニア",
        "position": "一般",
        "department": "開発部",
        "age": 25,
        "hire_date": "2026-04-01",
    }
    client.post("/api/employees", json=payload)
    response = client.get("/api/employees")
    assert response.status_code == 200
    names = [e["name"] for e in response.get_json()]
    assert "新田一郎" in names


def test_必須フィールド欠落で400が返る(client):
    payload = {"name": "新田一郎"}
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_nameが空文字で400が返る(client):
    payload = {
        "name": "",
        "role": "エンジニア",
        "position": "一般",
        "department": "開発部",
        "age": 25,
        "hire_date": "2026-04-01",
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_ageに負の値で400が返る(client):
    payload = {
        "name": "新田一郎",
        "role": "エンジニア",
        "position": "一般",
        "department": "開発部",
        "age": -1,
        "hire_date": "2026-04-01",
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_hire_dateのフォーマット不正で400が返る(client):
    payload = {
        "name": "新田一郎",
        "role": "エンジニア",
        "position": "一般",
        "department": "開発部",
        "age": 25,
        "hire_date": "20260401",
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()
