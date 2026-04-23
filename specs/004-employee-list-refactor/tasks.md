---
description: "Task list for 社員一覧リファクタリング"
---

# Tasks: 社員一覧リファクタリング

**Input**: Design documents from `specs/004-employee-list-refactor/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅

---

## Phase 1: Setup

**Purpose**: flask-injector の依存追加

- [X] T001 requirements.txt に `flask-injector` を追記（`flask==3.1.0` の次の行）

---

## Phase 2: Foundational（新規ファイル作成・既存コード変更なし）

**Purpose**: インターフェース・具象実装・DI設定の骨格を作る。既存コードは一切変更しないため既存テストはこの段階でも Green を維持する。

⚠️ この Phase が完了してから Phase 3 へ進む

- [X] T002 [P] app/api/domain/repository/__init__.py を新規作成（空ファイル）
- [X] T003 [P] app/api/domain/repository/employee_repository.py を新規作成（`@dataclass Employee` + `IEmployeeRepository(ABC)` を plan.md の実装方針に従い記述）
- [X] T004 [P] app/api/infrastructure/repository/__init__.py を新規作成（空ファイル）
- [X] T005 [P] app/api/infrastructure/repository/employee_repository.py を新規作成（`SQLiteEmployeeRepository(IEmployeeRepository)` を実装。`current_app._get_current_object()` 経由で `get_db()` を呼び、find_all と find_by_id を実装）
- [X] T006 app/module.py を新規作成（`AppModule(Module)`: `IEmployeeRepository → SQLiteEmployeeRepository` をバインド）

---

## Phase 3: User Story 1 - 外部動作維持（Priority: P1）🎯 MVP

**Goal**: リファクタリング後も社員一覧・詳細 API の外部仕様が変わらないことを保証する

**Independent Test**: `docker compose exec app pytest tests/presentation/test_employees.py -v` で全テスト Green

### Tests for User Story 1（TDD: 既存テストが Red → Green サイクルの基盤）

> **NOTE: 既存テスト（`tests/presentation/test_employees.py`）が Test Suite として機能する。T008〜T011 の変更で一時的に Red になることを確認し、T011 完了で Green に戻す。**

### Implementation for User Story 1

- [X] T007 [US1] app/api/usecase/get_employees.py を `GetEmployeesUseCase` クラスに変更（コンストラクタで `IEmployeeRepository` を受け取り、`execute()` メソッドで `repo.find_all()` を呼ぶ）
- [X] T008 [US1] app/api/usecase/get_employee.py を `GetEmployeeUseCase` クラスに変更（コンストラクタで `IEmployeeRepository` を受け取り、`execute(employee_id)` で `repo.find_by_id()` を呼ぶ）
- [X] T009 [US1] app/api/presentation/employees.py を更新（`from flask_injector import inject` を追加、`list_employees` と `get_employee_by_id` に `@inject` を付与、引数でユースケースクラスを受け取る形に変更）
- [X] T010 [US1] app/__init__.py を更新（`from flask_injector import FlaskInjector` と `from app.module import AppModule` を追加、`app.register_blueprint` の後に `FlaskInjector(app=app, modules=[AppModule()])` を追加）
- [ ] T011 [US1] 全テストが Green であることを確認（`docker compose exec app pytest tests/presentation/test_employees.py -v`）

**Checkpoint**: T011 完了時点で US1 は独立してテスト可能

---

## Phase 4: User Story 2 - インターフェース分離の検証（Priority: P2）

**Goal**: `GetEmployeesUseCase` にモック `IEmployeeRepository` を注入し、インフラ実装なしで動作することを証明する

**Independent Test**: `tests/presentation/test_employees.py` のモックテストが Green

### Tests for User Story 2（TDD: Red → Green）

> **NOTE: T012 のテストを先に書き、失敗（Red）を確認してから T013 で Green を確認する**

- [X] T012 [US2] tests/presentation/test_employees.py にモック注入テストを追記（先に書く・Red を確認）:
  - `FakeEmployeeRepository(IEmployeeRepository)` を定義（`find_all` が固定データを返す）
  - `GetEmployeesUseCase(FakeEmployeeRepository())` を直接インスタンス化して `execute()` を呼ぶ
  - 結果が期待通りであることを assert する
  - ※ `conftest.py` の Flask app fixture は不要（純粋なユニットテスト）
- [ ] T013 [US2] `docker compose exec app pytest tests/presentation/test_employees.py -v` で T012 のテストが Green であることを確認

**Checkpoint**: T013 完了で US2 独立検証完了

---

## Phase 5: User Story 3 - DI設定の一元管理（Priority: P3）

**Goal**: バインディング設定が `app/module.py` の単一ファイルにまとまっていることを確認する

**Independent Test**: `app/module.py` を参照するだけで全バインディングが把握できること

### Implementation for User Story 3

- [X] T014 [US3] app/module.py のバインディングが唯一の定義箇所であることを検証（`grep -r "binder.bind" app/` を実行し、`module.py` 以外にバインディングがないことを確認）

---

## Phase 6: Polish & Cleanup

**Purpose**: 移行完了後の旧ファイル削除と最終検証

- [X] T015 app/api/domain/employee.py を削除（エンティティは `domain/repository/employee_repository.py` に移行済み）
- [X] T016 app/api/infrastructure/employee_repository.py を削除（具象実装は `infrastructure/repository/employee_repository.py` に移行済み）
- [ ] T017 `docker compose exec app ruff check .` で静的解析エラーを修正（import 更新漏れなど）
- [ ] T018 `docker compose exec app pytest -v` で全テストの最終 Green を確認

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 依存なし → すぐ開始可能
- **Foundational (Phase 2)**: Phase 1 完了後 → 全 US をブロック
- **US1 (Phase 3)**: Phase 2 完了必須
- **US2 (Phase 4)**: Phase 3 完了必須（usecase クラスが存在していること）
- **US3 (Phase 5)**: Phase 2 完了後に検証可能
- **Polish (Phase 6)**: Phase 3〜5 全完了後

### User Story Dependencies

- **US1 (P1)**: Phase 2 完了後すぐ着手可能・最優先
- **US2 (P2)**: US1 完了依存（usecase クラスが必要）
- **US3 (P3)**: Phase 2 完了後に確認可能（独立）

### Within Phase 3 (US1)

- T007・T008 は並列実行可能（異なるファイル）
- T009 は T007・T008 完了後（ユースケースクラスを参照するため）
- T010 は T009 完了後（Blueprint の DI が確立してから FlaskInjector を初期化）
- T011 は T010 完了後（最終 Green 確認）

### Parallel Opportunities

```bash
# Phase 2: 全タスク並列実行可能
T002 domain/repository/__init__.py 作成
T003 domain/repository/employee_repository.py 作成
T004 infrastructure/repository/__init__.py 作成
T005 infrastructure/repository/employee_repository.py 作成
# T006 は T003・T005 完了後（import が必要）

# Phase 3 US1: T007・T008 並列
T007 get_employees.py クラス化
T008 get_employee.py クラス化
```

---

## Implementation Strategy

### MVP（US1 のみ）

1. Phase 1: Setup（requirements.txt）
2. Phase 2: Foundational（新規ファイル作成）
3. Phase 3: US1（既存テスト Green を保ちながらリファクタリング）
4. **STOP & VALIDATE**: 全テスト Green → MVP 完成
5. Polish（旧ファイル削除・ruff）

### 完全実装

1. MVP 完了後
2. Phase 4 (US2): モックテスト追加・インターフェース分離証明
3. Phase 5 (US3): DI一元管理確認
4. Phase 6: 最終クリーンアップ

---

## Notes

- `[P]` = 別ファイル・依存なしで並列実行可能
- `[USn]` = 対応するユーザーストーリー
- TDD: テストが Red であることを確認してから実装（Green）へ進む
- `seed()` 関数と `conftest.py` は変更不要（`get_db(app)` を直接使用するため）
- 旧ファイル削除（T015・T016）は全テスト Green 確認後に行う
