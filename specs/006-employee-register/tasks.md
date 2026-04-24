# Tasks: 社員登録機能

**Input**: Design documents from `/specs/006-employee-register/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**TDD必須**: Constitution大前提により、全テストタスクは対応する実装タスクより先に実行し、**必ずRed（失敗）を確認してから**実装に進む。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並列実行可能（別ファイル、依存なし）
- **[US1]**: User Story 1「社員情報を登録する」に対応

---

## Phase 1: Setup（既存プロジェクト確認）

**Purpose**: 既存プロジェクト構造の確認（新規セットアップ不要）

- [X] T001 既存テストが全てパスすることを確認する（`docker compose exec app-container pytest -v`）

---

## Phase 2: Foundational（共有インフラ変更）

**Purpose**: 全ユースケース実装の前提となるドメイン層の拡張

**⚠️ CRITICAL**: このフェーズ完了前にUser Story実装を開始してはならない

- [X] T002 `app/api/core/domain/employee/__init__.py` に `EmployeeCreateOutput` dataclass を追加する（フィールド: id, name, role, position, department, age, hire_date, status）
- [X] T003 `app/api/core/domain/repository/employee_repository.py` の `IEmployeeRepository` に `save(input) -> Employee` 抽象メソッドを追加する

**Checkpoint**: domain層変更完了 — 既存テストが引き続きパスすること

---

## Phase 3: User Story 1 - 社員情報を登録する (Priority: P1) 🎯 MVP

**Goal**: `POST /api/employees` で社員を登録し、`EmployeeCreateOutput` を201で返す

**Independent Test**: `docker compose exec app-container pytest tests/presentation/test_employees.py tests/core/usecase/employee/ -v` で全テストがパスすること

### TDD: テスト先行実装（Red フェーズ）⚠️

> **必ず FAIL を確認してから実装フェーズに進む（Constitution大前提）**

- [X] T004 [P] [US1] `tests/presentation/test_employees.py` に POST /api/employees の正常系テストを追加する（201, EmployeeCreateOutput フィールド確認, status="在籍中", years_of_service 不在確認）
- [X] T005 [P] [US1] `tests/presentation/test_employees.py` に POST /api/employees の異常系テストを追加する（必須フィールド欠落→400, age負値→400, hire_date形式不正→400）
- [X] T006 [US1] `tests/core/usecase/employee/test_create_employee.py` を新規作成し、CreateEmployeeUseCase の正常系テストを追加する（DBへの永続化・EmployeeCreateOutput返却確認）

**Red 確認**: `docker compose exec app-container pytest tests/presentation/test_employees.py tests/core/usecase/employee/test_create_employee.py -v` を実行し、全テストが FAIL することを確認する

---

### 実装（Green フェーズ）

- [X] T007 [US1] `app/api/infrastructure/repository/employee_repository.py` の `SQLiteEmployeeRepository` に `save(input)` を実装する（EmployeeModel作成・コミット・Employee エンティティ返却）
- [X] T008 [P] [US1] `app/api/core/usecase/employee/__init__.py` に `ICreateEmployeeUseCase` インターフェースを追加する（`execute(input) -> EmployeeCreateOutput`）
- [X] T009 [US1] `app/api/core/usecase/employee/create_employee.py` を新規作成し `CreateEmployeeUseCase` を実装する（IEmployeeRepository.save() 呼び出し・EmployeeCreateOutput 変換）
- [X] T010 [US1] `app/module.py` に `ICreateEmployeeUseCase → CreateEmployeeUseCase` の DI バインディングを追加する
- [X] T011 [US1] `app/api/presentation/employees.py` に `POST /api/employees` ルートを追加する（バリデーション・usecase 呼び出し・201/400/500 レスポンス）

**Green 確認**: `docker compose exec app-container pytest -v` を実行し、全テストがパスすることを確認する

**Checkpoint**: User Story 1 完了 — POST /api/employees が機能し、全テストがパスする

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: リグレッション確認・コード品質チェック

- [ ] T012 ruff format・ruff check を実行しコード品質を確認する（`docker compose exec app-container ruff format . && docker compose exec app-container ruff check .`）
- [ ] T013 全テストスイートでリグレッションがないことを確認する（`docker compose exec app-container pytest -v`）
<!-- Dockerが停止しているため手動実行が必要 -->

---

## Dependencies & Execution Order

### フェーズ依存関係

- **Phase 1**: 依存なし — 即時開始可能
- **Phase 2**: Phase 1 完了後 — User Story 実装をブロック
- **Phase 3**: Phase 2 完了後 — TDD順序（T004-T006 → Red確認 → T007-T011）
- **Phase 4**: Phase 3 完了後

### Phase 3 内の実行順序

```
T004, T005, T006 （並列可 — テスト先行）
  ↓ Red確認
T007, T008 （並列可 — 別ファイル）
  ↓
T009 （T007, T008 完了後）
  ↓
T010 （T009 完了後）
  ↓
T011 （T010 完了後）
  ↓ Green確認
```

### 並列実行例

```bash
# テスト先行（並列）
Task T004: tests/presentation/test_employees.py に正常系テスト追加
Task T005: tests/presentation/test_employees.py に異常系テスト追加
Task T006: tests/core/usecase/employee/test_create_employee.py 新規作成

# 実装（一部並列）
Task T007: SQLiteEmployeeRepository.save() 実装
Task T008: ICreateEmployeeUseCase インターフェース追加
```

---

## Implementation Strategy

### MVP（User Story 1のみ）

1. Phase 1: 既存テスト確認
2. Phase 2: Foundational（EmployeeCreateOutput + save() インターフェース追加）
3. Phase 3: TDD実装（Red→Green）
4. Phase 4: Polish
5. **VALIDATE**: `pytest -v` で全テストパス確認

---

## Notes

- [P] = 別ファイル・依存なし → 並列実行可能
- [US1] = User Story 1「社員情報を登録する」
- Constitution大前提: テストなしの実装コードは追加不可（MUST NOT）
- バリデーションは presentation 層で最小限に実施（Constitution III）
- 型アノテーションは記述しない（Constitution III）
- ロギングは追加しない（Constitution III）
