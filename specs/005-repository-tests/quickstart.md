# Quickstart: リポジトリ層・ユースケース層テスト + SQLAlchemy移行

## テスト実行

```bash
# リポジトリテストのみ
docker compose exec app pytest tests/infrastructure/repository/ -v

# ユースケーステストのみ
docker compose exec app pytest tests/usecase/ -v

# 全テスト（既存 + 新規）
docker compose exec app pytest -v

# 静的解析
docker compose exec app ruff check .
```

## 期待する出力（実装完了後）

```
tests/infrastructure/repository/test_employee_repository.py::test_find_all_在籍中のみ返す PASSED
tests/infrastructure/repository/test_employee_repository.py::test_find_all_空リストを返す PASSED
tests/infrastructure/repository/test_employee_repository.py::test_find_all_全フィールドが含まれる PASSED
tests/infrastructure/repository/test_employee_repository.py::test_find_by_id_在籍中社員を返す PASSED
tests/infrastructure/repository/test_employee_repository.py::test_find_by_id_退職済は返さない PASSED
tests/infrastructure/repository/test_employee_repository.py::test_find_by_id_存在しないIDはNone PASSED
tests/usecase/employee/test_find_employee_list.py::test_全フィールドが正確にマッピングされる PASSED
tests/usecase/employee/test_find_employee_list.py::test_勤続年数が正確に計算される PASSED
tests/usecase/employee/test_find_employee_list.py::test_在籍中社員のみが返される PASSED
tests/usecase/employee/test_find_employee_detail.py::test_在籍中社員の詳細が取得できる PASSED
tests/usecase/employee/test_find_employee_detail.py::test_存在しないIDはNoneを返す PASSED
tests/usecase/employee/test_find_employee_detail.py::test_退職済み社員はNoneを返す PASSED
```

## 変更対象ファイル

### 新規作成
- `app/api/infrastructure/models/__init__.py` — `Base`（DeclarativeBase）
- `app/api/infrastructure/models/employee_model.py` — `EmployeeModel`（ORMモデル）
- `tests/usecase/__init__.py`
- `tests/usecase/employee/__init__.py`
- `tests/usecase/employee/test_find_employee_list.py`
- `tests/usecase/employee/test_find_employee_detail.py`

### 変更
- `app/api/infrastructure/database.py` — SQLAlchemy session管理に切り替え
- `app/api/infrastructure/repository/employee_repository.py` — SQLAlchemy sessionを使うよう更新
- `app/__init__.py` — `DATABASE_URL` キーに変更、`init_db` の呼び出し更新
- `tests/conftest.py` — `db_session` fixture追加、`database_url` をSQLAlchemy URL形式に変更
- `tests/infrastructure/repository/test_employee_repository.py` — seedをSQLAlchemy経由に変更
- `tests/presentation/test_employees.py` — seedをSQLAlchemy経由に変更、モックテスト3件削除

### 削除
- `app/api/infrastructure/schema.sql` — `Base.metadata.create_all()` で代替

## アーキテクチャ図

```
tests/
├── conftest.py                                   # app / db_session fixture
├── presentation/
│   └── test_employees.py                         # HTTPレイヤー（SQLAlchemy seed）
├── infrastructure/
│   └── repository/
│       └── test_employee_repository.py           # リポジトリ直接テスト
└── usecase/
    └── employee/
        ├── test_find_employee_list.py            # FindEmployeeListUseCase 統合テスト
        └── test_find_employee_detail.py          # FindEmployeeDetailUseCase 統合テスト

app/api/infrastructure/
├── database.py                                   # SQLAlchemy engine/session管理
├── models/
│   ├── __init__.py                               # Base（DeclarativeBase）
│   └── employee_model.py                         # EmployeeModel
└── repository/
    └── employee_repository.py                    # SQLiteEmployeeRepository（SQLAlchemy使用）
```

## 注意点

- テストは `app.app_context()` 内で実行する（`current_app` が必要なため）
- モック不使用。全テストが実際のSQLite DBを操作して検証する
- `app` fixture はテストごとに一時SQLiteファイルを作成するためテスト間干渉なし
- `db_session` fixture は `app` fixture が生成した同一DBファイルを参照する
