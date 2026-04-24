# Quickstart: 社員登録機能 テストシナリオ

**Feature**: 社員登録機能（#22）
**Date**: 2026-04-24

## セットアップ

```bash
docker compose up -d
docker compose exec app-container pytest -v
```

---

## テストシナリオ

### シナリオ 1: 正常登録（Presentation層）

```python
def test_create_employee_success(client):
    payload = {
        "name": "山田 太郎",
        "role": "エンジニア",
        "position": "主任",
        "department": "開発部",
        "age": 30,
        "hire_date": "2020-04-01"
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "山田 太郎"
    assert data["status"] == "在籍中"
    assert "id" in data
    assert "years_of_service" not in data
```

### シナリオ 2: 必須フィールド欠落（Presentation層）

```python
def test_create_employee_missing_field(client):
    payload = {"name": "山田 太郎"}  # 他フィールドなし
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()
```

### シナリオ 3: age に負の値（Presentation層）

```python
def test_create_employee_negative_age(client):
    payload = {
        "name": "山田 太郎", "role": "エンジニア",
        "position": "主任", "department": "開発部",
        "age": -1, "hire_date": "2020-04-01"
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
```

### シナリオ 4: hire_date フォーマット不正（Presentation層）

```python
def test_create_employee_invalid_hire_date(client):
    payload = {
        "name": "山田 太郎", "role": "エンジニア",
        "position": "主任", "department": "開発部",
        "age": 30, "hire_date": "20200401"  # YYYY-MM-DD でない
    }
    response = client.post("/api/employees", json=payload)
    assert response.status_code == 400
```

### シナリオ 5: ユースケース正常実行（UseCase層）

```python
def test_create_employee_usecase(db_session):
    # リポジトリ経由でDBに保存できることを確認
    repo = SQLiteEmployeeRepository(db_session)
    input = EmployeeInput(
        name="佐藤 花子", role="デザイナー",
        position="リーダー", department="デザイン部",
        age=28, hire_date="2022-04-01"
    )
    usecase = CreateEmployeeUseCase(repo)
    result = usecase.execute(input)
    assert result.name == "佐藤 花子"
    assert result.status == "在籍中"
    assert result.id is not None
```

### シナリオ 6: 既存GETエンドポイントのリグレッション確認

```bash
docker compose exec app-container pytest tests/presentation/test_employees.py -v
# 全テストがパスすること（既存テスト含む）
```

---

## 検証ポイント

- 201レスポンスに `status: "在籍中"` が含まれること
- 201レスポンスに `years_of_service` が含まれないこと
- 400エラーのレスポンスが `{"error": "..."}` 形式であること
- 登録後に `GET /api/employees` で一覧に表示されること
