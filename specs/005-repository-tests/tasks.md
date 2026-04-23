---
description: "Task list for リポジトリ層・ユースケース層テスト + SQLAlchemy移行"
---

# Tasks: リポジトリ層・ユースケース層テスト + SQLAlchemy移行

**Input**: Design documents from `specs/005-repository-tests/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ quickstart.md ✅

---

## Phase 1: Setup（SQLAlchemy基盤の新規作成）

**Purpose**: SQLAlchemy ORM モデルと依存関係の準備

- [X] T001 pyproject.toml の dependencies に `sqlalchemy` を追加する
- [X] T002 [P] `app/api/infrastructure/models/__init__.py` を新規作成し `Base`（DeclarativeBase）を定義する
- [X] T003 [P] `app/api/infrastructure/models/employee_model.py` を新規作成し `EmployeeModel`（Column スタイル、`__table_args__` に status CHECK 制約）を定義する

**Checkpoint**: EmployeeModel が定義され、`Base.metadata.create_all()` が実行できる状態

---

## Phase 2: Foundational（既存 infrastructure 層の SQLAlchemy 移行）

**Purpose**: アプリケーション本体を SQLAlchemy session ベースに切り替える。全ユーザーストーリーの前提条件。

⚠️ **CRITICAL**: このフェーズが完了するまで既存テストは壊れた状態になる。一気に進めること。

- [X] T004 `app/api/infrastructure/database.py` を書き換える。`get_db()` を削除し `get_session(app)` を実装する。`init_db(app)` は `Base.metadata.create_all(engine)` でスキーマを生成し、teardown で session を close するよう変更する
- [X] T005 `app/__init__.py` を変更する。`database_url` パラメータを SQLAlchemy URL 形式（`sqlite:///path`）で受け取り `app.config["DATABASE_URL"]` に格納する。`schema.sql` の読み込みを削除する
- [X] T006 `app/api/infrastructure/repository/employee_repository.py` を書き換える。`get_db()` の代わりに `get_session(current_app._get_current_object())` を使い、SQLAlchemy の `session.query(EmployeeModel)` でクエリを実行する。`EmployeeModel` → `Employee` の変換は `_to_entity()` メソッドで行う
- [X] T007 `app/api/infrastructure/schema.sql` を削除する（`Base.metadata.create_all()` で代替済み）

**Checkpoint**: アプリケーションが SQLAlchemy 経由で起動できる状態

---

## Phase 3: US4 - 既存テストの SQLAlchemy 移行 (Priority: P1)

**Goal**: 既存の全テストの seeding を SQLAlchemy session 経由に切り替え、全テストが Green を維持する

**Independent Test**: `docker compose exec app pytest -v` で既存の全テストが Green（新テスト追加前の状態）

- [X] T008 [US4] `tests/conftest.py` を変更する。`db_session` fixture を追加し（`create_engine(app.config["DATABASE_URL"])` → `sessionmaker` → `Session()` を yield）、既存 `app` fixture の `database_url=db_path` を `database_url=f"sqlite:///{db_path}"` に変更する
- [X] T009 [US4] `tests/infrastructure/repository/test_employee_repository.py` を変更する。`seed()` 関数を `db_session` fixture 経由の SQLAlchemy seeding（`db_session.add(EmployeeModel(...)); db_session.commit()`）に書き換える。`get_db()` の import を削除する。`test_find_by_id_退職済は返さない` の生 SQL による ID 取得も SQLAlchemy 経由に変更する
- [X] T010 [US4] `tests/presentation/test_employees.py` を変更する。`seed()` / `seed_one()` 関数を SQLAlchemy seeding に書き換える。`FakeEmployeeRepository` クラスと以下のモックテスト 3 件を削除する: `test_モックリポジトリを注入してFindEmployeeListUseCaseが動作する`・`test_モックリポジトリを注入してFindEmployeeDetailUseCaseが動作する`・`test_存在しないIDはモックリポジトリでNoneを返す`

**Checkpoint**: T010 完了時点で `docker compose exec app pytest -v` が全て Green（US4 独立検証完了）

---

## Phase 4: US1 - リポジトリ正常系テスト（既存実装の確認）(Priority: P1) 🎯

**Goal**: SQLAlchemy 移行後もリポジトリ正常系テストが正しく動作することを確認する

**Independent Test**: `docker compose exec app pytest tests/infrastructure/repository/ -v` で正常系 3 件が Green

**実装済みテスト（Phase 3 の移行対象）**:
- `test_find_all_在籍中のみ返す` ✅（実装済み、seeding 移行のみ）
- `test_find_all_空リストを返す` ✅（実装済み、seeding 移行のみ）
- `test_find_all_全フィールドが含まれる` ✅（実装済み、seeding 移行のみ）
- `test_find_by_id_在籍中社員を返す` ✅（実装済み、seeding 移行のみ）

- [ ] T011 [US1] `docker compose exec app pytest tests/infrastructure/repository/ -k "find_all or find_by_id_在籍中" -v` を実行し US1 正常系テストが全て Green であることを確認（Docker 上で実行）

**Checkpoint**: T011 完了で US1 独立検証完了

---

## Phase 5: US2 - リポジトリ異常系テスト（既存実装の確認）(Priority: P2)

**Goal**: SQLAlchemy 移行後もリポジトリ異常系テストが正しく動作することを確認する

**Independent Test**: `docker compose exec app pytest tests/infrastructure/repository/ -v` で異常系 2 件が Green

**実装済みテスト（Phase 3 の移行対象）**:
- `test_find_by_id_退職済は返さない` ✅（実装済み、seeding 移行のみ）
- `test_find_by_id_存在しないIDはNone` ✅（実装済み、変更不要）

- [ ] T012 [US2] `docker compose exec app pytest tests/infrastructure/repository/ -v` を実行し US2 異常系テストが全て Green であることを確認（Docker 上で実行）

**Checkpoint**: T012 完了で US2 独立検証完了

---

## Phase 6: US3 - ユースケース層インテグレーションテスト (Priority: P2)

**Goal**: `FindEmployeeListUseCase` と `FindEmployeeDetailUseCase` を実 DB を使ってインテグレーションテストする

**Independent Test**: `docker compose exec app pytest tests/usecase/ -v` で全 6 件が Green

- [X] T013 [P] [US3] `tests/usecase/__init__.py` と `tests/usecase/employee/__init__.py` を新規作成する（空ファイル）
- [X] T014 [P] [US3] `tests/usecase/employee/test_find_employee_list.py` を新規作成する。`db_session` fixture でデータを seeding し `app.app_context()` 内で `FindEmployeeListUseCase(SQLiteEmployeeRepository()).execute()` を呼んで以下を検証する:
  - `test_全フィールドが正確にマッピングされる`: `EmployeeOutput` の全フィールド（id/name/role/position/department/age/hire_date/years_of_service）が正確に設定されていること
  - `test_勤続年数が正確に計算される`: hire_date が既知の社員で `years_of_service` が正しく計算されること（端数切り捨て）
  - `test_在籍中社員のみが返される`: 退職済み社員が結果に含まれないこと
- [X] T015 [P] [US3] `tests/usecase/employee/test_find_employee_detail.py` を新規作成する。`db_session` fixture でデータを seeding し `app.app_context()` 内で `FindEmployeeDetailUseCase(SQLiteEmployeeRepository()).execute(id)` を呼んで以下を検証する:
  - `test_在籍中社員の詳細が取得できる`: 正しい `EmployeeOutput` が返ること
  - `test_存在しないIDはNoneを返す`: ID=9999 で `None` が返ること
  - `test_退職済み社員はNoneを返す`: 退職済み社員のIDで `None` が返ること
- [ ] T016 [US3] `docker compose exec app pytest tests/usecase/ -v` を実行し US3 の全テストが Green であることを確認（Docker 上で実行）

**Checkpoint**: T016 完了で US3 独立検証完了

---

## Phase 7: Polish & 最終検証

**Purpose**: 全テストの共存確認・静的解析

- [ ] T017 `docker compose exec app pytest -v` を実行し全テストが Green であることを確認
- [ ] T018 `docker compose exec app ruff check .` を実行し静的解析エラーがないことを確認

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 依存なし → T002・T003 は並列実行可能
- **Foundational (Phase 2)**: Phase 1 完了後（T004→T005→T006→T007 の順）
- **US4 (Phase 3)**: Phase 2 完了後（T008→T009→T010 の順）
- **US1 (Phase 4)**: Phase 3 完了後
- **US2 (Phase 5)**: Phase 4 完了後
- **US3 (Phase 6)**: Phase 3 完了後（T013・T014・T015 は並列可能）
- **Polish (Phase 7)**: Phase 4・5・6 全て完了後

### User Story Dependencies

- **US4 (P1)**: Phase 2 完了後 → US1・US2・US3 の前提
- **US1 (P1)**: US4 完了後（既存テストのSQLAlchemy移行確認）
- **US2 (P2)**: US4 完了後（既存テストのSQLAlchemy移行確認）
- **US3 (P2)**: US4 完了後（新規ユースケーステスト）

### Parallel Opportunities

```bash
# Phase 1: T002・T003 並列実行可能
T002: app/api/infrastructure/models/__init__.py（Base）
T003: app/api/infrastructure/models/employee_model.py（EmployeeModel）

# Phase 6: T013・T014・T015 並列実行可能
T013: tests/usecase/__init__.py 系
T014: tests/usecase/employee/test_find_employee_list.py
T015: tests/usecase/employee/test_find_employee_detail.py
```

---

## Implementation Strategy

### MVP First（US4 + US1 のみ）

1. Phase 1: Setup（SQLAlchemy依存追加・モデル定義）
2. Phase 2: Foundational（database.py・app/__init__.py・リポジトリ実装更新）
3. Phase 3: US4（既存テストのseeding移行・モックテスト削除）
4. Phase 4: US1 確認
5. **STOP & VALIDATE**: `pytest -v` → 既存テスト全 Green

### 完全実装

1. MVP 完了後
2. Phase 5: US2 確認
3. Phase 6: US3（ユースケーステスト6件追加）
4. Phase 7: 最終検証

---

## Notes

- `[P]` = 別ファイルで並列実行可能
- `[USn]` = 対応するユーザーストーリー
- Phase 2 は「一気に進める」こと（途中で既存テストが壊れる期間が発生する）
- `EmployeeModel` は `Column` スタイルを使用（型アノテーション非使用、Constitution III 準拠）
- `db_session` fixture は `app` fixture の一時 SQLite ファイルと同じ DB を参照する
- ユースケーステストは `SQLiteEmployeeRepository()` を直接インスタンス化して注入する
- `schema.sql` 削除後は `Base.metadata.create_all()` でスキーマ管理する
