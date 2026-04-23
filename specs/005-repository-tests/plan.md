# Implementation Plan: リポジトリ層・ユースケース層テスト + SQLAlchemy移行

**Branch**: `feature/issues-15` | **Date**: 2026-04-23 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `specs/005-repository-tests/spec.md`

## Summary

SQLAlchemy ORM（DeclarativeBase + Column スタイル）を infrastructure 層に導入し、
`SQLiteEmployeeRepository` を生SQL から ORM ベースに移行する。
合わせてリポジトリ層・ユースケース層の統合テストを実DB（SQLite）で実装し、
既存のモックベーステストを削除して一貫したテスト戦略に統一する。

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Flask 3.1、SQLAlchemy 2.x、injector 0.22.0、pytest 8.3.5  
**Storage**: SQLite（SQLAlchemy経由）  
**Testing**: pytest（実DBインテグレーションテスト、モック不使用）  
**Target Platform**: Docker（Linux）  
**Project Type**: web-service  
**Performance Goals**: N/A（テスト追加のみ）  
**Constraints**: DBはSQLiteのみ（Constitution III）、型アノテーションは最小限（Constitution III）  
**Scale/Scope**: 既存6テスト + 新規6テスト = 合計12テスト（リポジトリ・ユースケース）

## Constitution Check

| 原則 | 評価 | 備考 |
|------|------|------|
| I. クリーンアーキテクチャ | ✅ PASS | `EmployeeModel` は infrastructure 層のみ。domain 層は変更なし |
| II. Blueprintパターン | ✅ PASS | presentation 層変更なし |
| III. シンプリシティ | ✅ PASS | DBはSQLiteのまま。ORM導入はユーザー明示指示により正当化。型アノテーション非使用の `Column` スタイルを採用 |
| IV. 日本語ドキュメント | ✅ PASS | |
| V. インターフェース分離・DI | ✅ PASS | `IEmployeeRepository` インターフェースは変更なし。session管理は `g` 経由でinfrastructure内に閉じる |
| TDD大前提 | ✅ PASS | テスト先行で実装する |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| SQLAlchemy ORM導入（YAGNI軽微違反） | ユーザー明示指示。テストのseeding統一と将来DB移行耐性 | 生SQLiteのままではテストとの整合性が取れない |

## Project Structure

### Documentation (this feature)

```text
specs/005-repository-tests/
├── plan.md              # このファイル
├── research.md          # Phase 0 出力
├── data-model.md        # Phase 1 出力
├── quickstart.md        # Phase 1 出力
└── tasks.md             # Phase 2 出力（/speckit.tasks で生成）
```

### Source Code (repository root)

```text
app/
└── api/
    ├── domain/
    │   ├── employee/
    │   │   ├── __init__.py        # EmployeeInput / EmployeeOutput DTO（変更なし）
    │   │   └── employee.py        # Employee エンティティ（変更なし）
    │   └── repository/
    │       └── employee_repository.py  # IEmployeeRepository（変更なし）
    ├── infrastructure/
    │   ├── database.py            # 【変更】SQLAlchemy engine/session 管理に切り替え
    │   ├── models/                # 【新規】
    │   │   ├── __init__.py        # Base（DeclarativeBase）
    │   │   └── employee_model.py  # EmployeeModel（ORM定義）
    │   └── repository/
    │       └── employee_repository.py  # 【変更】SQLAlchemy session 使用に更新
    ├── usecase/
    │   └── employee/              # 変更なし
    └── presentation/
        └── employees.py           # 変更なし
app/__init__.py                    # 【変更】DATABASE_URL キーに更新
app/module.py                      # 変更なし

tests/
├── conftest.py                    # 【変更】db_session fixture 追加
├── presentation/
│   └── test_employees.py          # 【変更】seed を SQLAlchemy 経由に変更、モックテスト3件削除
├── infrastructure/
│   └── repository/
│       └── test_employee_repository.py  # 【変更】seed を SQLAlchemy 経由に変更
└── usecase/                       # 【新規】
    ├── __init__.py
    └── employee/
        ├── __init__.py
        ├── test_find_employee_list.py   # FindEmployeeListUseCase 統合テスト
        └── test_find_employee_detail.py # FindEmployeeDetailUseCase 統合テスト

# 削除
app/api/infrastructure/schema.sql  # Base.metadata.create_all() で代替
```

**Structure Decision**: 既存のClean Architecture構造を維持。`models/` ディレクトリをinfrastructure層に追加し、`EmployeeModel` を配置する。テストは層ごとに `tests/infrastructure/` と `tests/usecase/` に整理する。

## 実装方針

### SQLAlchemy移行の順序

1. `Base` と `EmployeeModel` を作成（スキーマ定義）
2. `database.py` を SQLAlchemy session 管理に書き換え
3. `app/__init__.py` を `DATABASE_URL` 形式に更新
4. `SQLiteEmployeeRepository` を SQLAlchemy 使用に更新
5. `conftest.py` に `db_session` fixture 追加
6. 既存テストのseedを SQLAlchemy 経由に移行（全テストがGreenになることを確認）
7. ユースケーステストを追加
8. モックベーステストを削除

### ユースケーステストの設計

```python
# tests/usecase/employee/test_find_employee_list.py の例
def test_全フィールドが正確にマッピングされる(app, db_session):
    # seed
    db_session.add(EmployeeModel(name="山田太郎", ...))
    db_session.commit()

    with app.app_context():
        usecase = FindEmployeeListUseCase(SQLiteEmployeeRepository())
        result = usecase.execute()

    assert result[0].name == "山田太郎"
    assert result[0].years_of_service >= 0
```

### conftest.py の `db_session` fixture

```python
@pytest.fixture
def db_session(app):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(app.config["DATABASE_URL"])
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
```

### `database.py` の書き換え

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g

def get_session(app):
    if "db_session" not in g:
        engine = create_engine(app.config.get("DATABASE_URL", "sqlite:///employees.db"))
        Session = sessionmaker(bind=engine)
        g.db_session = Session()
    return g.db_session

def init_db(app):
    from app.api.infrastructure.models import Base
    engine = create_engine(app.config.get("DATABASE_URL", "sqlite:///employees.db"))
    Base.metadata.create_all(engine)

    @app.teardown_appcontext
    def close_session(e=None):
        session = g.pop("db_session", None)
        if session is not None:
            session.close()
```
