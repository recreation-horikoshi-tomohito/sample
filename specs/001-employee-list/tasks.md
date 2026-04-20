---
description: "社員一覧取得APIのタスクリスト"
---

# タスク: 社員一覧

**Input**: `specs/001-employee-list/` の設計ドキュメント
**Prerequisites**: plan.md ✅、spec.md ✅、research.md ✅、data-model.md ✅、contracts/ ✅

**TDD大前提**: 各ユーザーストーリーのテストを先に作成し、失敗（Red）を確認してから実装（Green）に進む。

## フォーマット: `[ID] [P?] [Story?] 説明`

- **[P]**: 並列実行可（異なるファイル、依存なし）
- **[Story]**: 対応するユーザーストーリー（例: US1、US2）

---

## Phase 1: セットアップ（共有インフラ）

**目的**: プロジェクトのディレクトリ構造とテスト基盤の整備

- [x] T001 ディレクトリ構造と `__init__.py` を作成する（`app/__init__.py`、`app/api/__init__.py`、`app/api/domain/__init__.py`、`app/api/usecase/__init__.py`、`app/api/infrastructure/__init__.py`、`app/api/presentation/__init__.py`、`tests/__init__.py`、`tests/presentation/__init__.py`）
- [x] T002 [P] Flaskアプリのファクトリ関数を作成する（`app/__init__.py`）
- [x] T003 [P] pytestの設定とFlaskテストクライアントのfixture を作成する（`tests/conftest.py`）

**チェックポイント**: `docker compose up -d` でコンテナが起動し、Flaskアプリが `http://localhost:8081` に応答する

---

## Phase 2: 基盤（全ユーザーストーリーの前提）

**目的**: 全ストーリーで共通利用するDB基盤の構築

**⚠️ 重要**: このフェーズが完了するまでユーザーストーリーの実装を開始してはならない

- [x] T004 SQLiteのスキーマ定義（`employees` テーブル）を作成する（`app/api/infrastructure/schema.sql`）
- [x] T005 DB接続・初期化処理（`get_db`、`init_db`）を実装する（`app/api/infrastructure/database.py`）
- [x] T006 アプリ起動時にDBを自動初期化する処理を追加する（`app/__init__.py`）

**チェックポイント**: コンテナ起動時に `employees` テーブルが自動作成される

---

## Phase 3: User Story 1 - 在籍中の社員一覧の取得（Priority: P1）🎯 MVP

**目標**: `GET /api/employees` で在籍中の社員一覧をJSON形式で返す。退職済の社員は含まない。

**Independent Test**: 在籍中・退職済の社員が混在するDBに対してAPIを呼び出し、在籍中の社員のみが返されることをpytestで確認できる。

### US1のテスト（TDD: 先に作成・失敗を確認すること）⚠️

> **大前提: T007を作成し、テストが失敗（Red）することを確認してから T008 以降の実装へ進む**

- [x] T007 [US1] 社員一覧取得のテストを作成する（`tests/presentation/test_employees.py`）
  - 在籍中の社員のみが返されること（US1-シナリオ1）
  - 退職済の社員が含まれないこと（US1-シナリオ2）
  - 在籍中の社員が0名のとき空配列が返されること（US1-シナリオ3）

### US1の実装（Green）

- [x] T008 [P] [US1] `Employee` エンティティを作成する（`app/api/domain/employee.py`）
- [x] T009 [P] [US1] `EmployeeRepository`（在籍中フィルタ付きSQLiteリポジトリ）を実装する（`app/api/infrastructure/employee_repository.py`）
- [x] T010 [US1] `GetEmployeesUseCase` を実装する（`app/api/usecase/get_employees.py`）
- [x] T011 [US1] `employees` Blueprint（`GET /api/employees`）を実装する（`app/api/presentation/employees.py`）
- [x] T012 [US1] `employees` Blueprint をアプリに登録する（`app/__init__.py`）

**チェックポイント**: T007のテストが全てパスし、`GET http://localhost:8081/api/employees` が在籍中の社員一覧をJSON形式で返す

---

## Phase 4: User Story 2 - 勤続年数の自動計算（Priority: P2）

**目標**: 各社員の `years_of_service` を `hire_date` から現在日付で自動計算してレスポンスに含める。

**Independent Test**: 入社日が異なる複数の社員に対してAPIを呼び出し、各社員の `years_of_service` が正確な年数（端数切り捨て）で返されることをpytestで確認できる。

### US2のテスト（TDD: 先に追加・失敗を確認すること）⚠️

> **大前提: T013を追加し、テストが失敗（Red）することを確認してから T014 以降の実装へ進む**

- [x] T013 [US2] 勤続年数計算のテストを追加する（`tests/presentation/test_employees.py`）
  - 入社日が5年前の社員の `years_of_service` が `5` で返されること（US2-シナリオ1）
  - 入社日が今年の社員の `years_of_service` が `0` で返されること（US2-シナリオ2）
  - 端数が切り捨てられること（エッジケース）

### US2の実装（Green）

- [x] T014 [US2] `Employee` エンティティに `years_of_service` 計算ロジックを追加する（`app/api/domain/employee.py`）
- [x] T015 [US2] `GetEmployeesUseCase` のレスポンス生成に `years_of_service` を組み込む（`app/api/usecase/get_employees.py`）

**チェックポイント**: T013のテストが全てパスし、レスポンスの `years_of_service` が正確な年数で返される

---

## Phase 5: ポリッシュ

**目的**: コード品質の確認と動作検証

- [x] T016 [P] `ruff check app/ tests/` で静的解析を実施し、指摘を解消する
- [x] T017 quickstart.mdの動作検証チェックリストを全て実行して確認する

---

## 依存関係と実行順序

### フェーズ依存

- **Phase 1（セットアップ）**: 依存なし → 即時開始可
- **Phase 2（基盤）**: Phase 1 完了に依存 → 全ユーザーストーリーをブロック
- **Phase 3（US1）**: Phase 2 完了に依存
- **Phase 4（US2）**: Phase 3 完了に依存（同一エンドポイントへの拡張のため）
- **Phase 5（ポリッシュ）**: 全フェーズ完了後

### ユーザーストーリー内の依存

```
[US1]
T007（テスト作成・Red確認）
  → T008, T009（並列実装可）
  → T010（T008, T009完了後）
  → T011（T010完了後）
  → T012（T011完了後）
  → T007テストがパス（Green）

[US2]
T013（テスト追加・Red確認）
  → T014
  → T015（T014完了後）
  → T013テストがパス（Green）
```

### 並列実行可能なタスク

| フェーズ | 並列実行可能なタスク |
|---------|-------------------|
| Phase 1 | T002、T003 |
| Phase 3 | T008、T009（T007完了後） |
| Phase 5 | T016 |

---

## 並列実行例: User Story 1

```bash
# ステップ1: テスト作成（先に失敗させる）
Task: "T007 社員一覧取得のテストを作成する（tests/presentation/test_employees.py）"
→ pytest tests/presentation/test_employees.py を実行してテストが失敗することを確認

# ステップ2: 並列実装（失敗確認後）
Task: "T008 Employee エンティティを作成する（app/api/domain/employee.py）"
Task: "T009 EmployeeRepository を実装する（app/api/infrastructure/employee_repository.py）"

# ステップ3: 順次実装（T008, T009完了後）
Task: "T010 GetEmployeesUseCase を実装する（app/api/usecase/get_employees.py）"
Task: "T011 employees Blueprint を実装する（app/api/presentation/employees.py）"
Task: "T012 Blueprint をアプリに登録する（app/__init__.py）"

# 確認
→ pytest tests/presentation/test_employees.py を実行してテストがパスすることを確認
```

---

## 実装戦略

### MVP優先（US1のみ）

1. Phase 1 セットアップ完了
2. Phase 2 基盤完了（**重要 — US1をブロック**）
3. T007: テスト作成 → 失敗確認（Red）
4. T008〜T012: 実装（Green）
5. **停止・検証**: `curl http://localhost:8081/api/employees` で在籍中社員のみ返ることを確認

### インクリメンタルデリバリー

1. Phase 1 + 2: 基盤完了
2. Phase 3（US1）: テスト→実装→確認 ← **ここまでがMVP**
3. Phase 4（US2）: テスト追加→実装→確認
4. Phase 5: ポリッシュ

---

## メモ

- [P] タスク = 異なるファイル・依存なし（並列実行可能）
- [Story] ラベルはユーザーストーリーとのトレーサビリティのため
- **TDD大前提**: テストの失敗（Red）を確認してから実装（Green）へ — これは非交渉
- `status` フィールドはレスポンスに含めない（フィルタリング専用）
- `years_of_service` はDBに保存せず、レスポンス生成時に計算する
