# Research: リポジトリ層・ユースケース層テスト + SQLAlchemy移行

## Decision 1: SQLAlchemy Sessionの管理方式

**Decision**: Flask `g` オブジェクトを使ったリクエストスコープのsession管理

**Rationale**:
- 既存の `get_db(app)` パターン（`g.db`）と整合する
- リクエストごとにsessionが作られ、teardownで自動クローズされる
- テスト時は `app.app_context()` 内で session が生成・破棄される

**Alternatives considered**:
- `scoped_session` + `threading.local`: Flask環境では `g` の方がシンプルで十分
- セッションをDIで注入: SQLAlchemy sessionはFlaskライフサイクルと密結合のため `g` 経由が適切

---

## Decision 2: SQLAlchemy ORM スタイル

**Decision**: `DeclarativeBase` + `Column`（非Mapped型表記）

**Rationale**:
- Constitution Principle III「型アノテーションは記述しない（SHOULD NOT）」に準拠するため、`mapped_column` のMapped型を使わず旧来の `Column` スタイルを採用
- `Base.metadata.create_all(engine)` でスキーマ自動生成 → `schema.sql` を廃止できる

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class EmployeeModel(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ...
```

**Alternatives considered**:
- `mapped_column` + `Mapped[str]` (SQLAlchemy 2.x推奨): 型アノテーション必須のため Constitution III 違反リスクあり → 不採用

---

## Decision 3: テスト分離方式

**Decision**: テストごとに一時SQLiteファイルを作成（既存方式を継承）

**Rationale**:
- 既存の `conftest.py` の `app` fixture（`tempfile.mkstemp`）をそのまま活用
- テストごとにファイルごと破棄するため完全な分離が保証される
- SQLAlchemy sessionも同一の一時ファイルに向けることで整合性を保つ

**Alternatives considered**:
- トランザクションロールバック方式: fixture複雑さが増す → 不採用
- インメモリSQLite (`sqlite:///:memory:`): テスト間でDB状態が共有されるリスク → 不採用

---

## Decision 4: conftest.py への `db_session` fixture 追加

**Decision**: `db_session` fixture を追加し、SQLAlchemy sessionをテストに提供

**Rationale**:
- seeding（テストデータ投入）をSQLAlchemy ORM経由で行うため
- `app.config["DATABASE_URL"]` にSQLAlchemy URL（`sqlite:///path`）を格納する

```python
@pytest.fixture
def db_session(app):
    engine = create_engine(app.config["DATABASE_URL"])
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
```

---

## Decision 5: create_app の変更

**Decision**: `database_url` パラメータをSQLAlchemy URL形式（`sqlite:///path`）に変更

**Rationale**:
- 従来: `db_path` (ファイルパス文字列) → `app.config["DATABASE"]`
- 変更後: `database_url` (SQLAlchemy URL文字列) → `app.config["DATABASE_URL"]`
- `init_db` が `Base.metadata.create_all(engine)` でスキーマ生成するため `schema.sql` は削除

---

## Decision 6: ユースケーステストの配置

**Decision**: `tests/usecase/employee/` 配下に `test_find_employee_list.py` / `test_find_employee_detail.py`

**Rationale**:
- クリーンアーキテクチャの層構造に対応した形でテストを整理
- ユースケーステストは実DBを使ったインテグレーションテスト（モックなし）
- `tests/infrastructure/repository/` と対称的な構造

---

## Decision 7: 既存モックテストの削除対象

`tests/presentation/test_employees.py` の以下を削除し、実DBテストに置き換える:
- `FakeEmployeeRepository` クラス定義
- `test_モックリポジトリを注入してFindEmployeeListUseCaseが動作する`
- `test_モックリポジトリを注入してFindEmployeeDetailUseCaseが動作する`
- `test_存在しないIDはモックリポジトリでNoneを返す`

---

## Decision 8: SQLiteEmployeeRepositoryの名称維持

**Decision**: クラス名 `SQLiteEmployeeRepository` を維持（SQLAlchemy使用後も変更しない）

**Rationale**:
- DBはSQLiteのまま（Constitution Principle III準拠）
- ORMはアクセス手段の変更であり、DBの変更ではない
- 既存のDIバインディング（module.py）への影響を最小化する
