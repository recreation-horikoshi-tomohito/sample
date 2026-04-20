# Tasks: 社員詳細機能

**Input**: `/specs/002-employee-detail/` の設計ドキュメント
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅
**GitHub Issue**: #10 | **ブランチ**: `feature/issues-10`

**大前提**: TDDによりテストを先行して書き、Red を確認してから実装（Green）に移行する。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並列実行可能（異なるファイル、依存なし）
- **[Story]**: 対応するユーザーストーリー（US1, US2）
- テストは常に実装より先に書き、Red を確認する

---

## Phase 1: Setup（セットアップ）

**目的**: 既存プロジェクトへの追加箇所を把握する

- [X] T001 実装対象ファイルパスを確認し、既存コード（app/api/domain/employee.py, app/api/infrastructure/employee_repository.py, app/api/presentation/employees.py）との接続点を把握する

---

## Phase 2: Foundational（基盤確認）

**目的**: 本機能に必要な既存インフラが流用可能であることを確認する

**⚠️ 注意**: 既存プロジェクトのため新規セットアップは不要。変更不要であることを確認するのみ。

- [X] T002 [P] 既存 Employee エンティティの to_dict() が years_of_service を含むことを app/api/domain/employee.py で確認する（変更なし）
- [X] T003 [P] 既存 DB スキーマ（app/api/infrastructure/schema.sql）に変更不要であることを確認する（status フィールド、id フィールドが存在すること）

**チェックポイント**: 基盤確認完了 → ユーザーストーリー実装へ

---

## Phase 3: US1 - 社員詳細情報の取得（優先度: P1）🎯 MVP

**目標**: 社員IDを指定して在籍中社員の詳細情報を取得できる

**独立テスト**: `GET /api/employees/<id>` に在籍中社員のIDを指定してリクエストし、全必須フィールドを含むJSONが返ることを確認する

### US1 のテスト（TDD: 先に書いて Red を確認）

- [X] T004 [US1] test_在籍中社員のIDを指定して詳細情報が取得できる（200 OK）テストを tests/presentation/test_employees.py に追記し、**Red を確認する**
- [X] T005 [P] [US1] test_詳細レスポンスに id・name・role・position・department・age・hire_date・years_of_service が含まれる テストを tests/presentation/test_employees.py に追記し、**Red を確認する**
- [X] T006 [P] [US1] test_詳細レスポンスに status フィールドが含まれない テストを tests/presentation/test_employees.py に追記し、**Red を確認する**

### US1 の実装（テスト Green を目指す）

- [X] T007 [US1] find_active_employee_by_id(app, employee_id) を app/api/infrastructure/employee_repository.py に追加する（WHERE id=? AND status='在籍中'、見つからない場合は None を返す）
- [X] T008 [US1] app/api/usecase/get_employee.py を新規作成し get_employee(app, employee_id) を実装する（None の場合は None を返す）
- [X] T009 [US1] GET /api/employees/<int:employee_id> エンドポイントを app/api/presentation/employees.py に追加し、T004〜T006 のテストが **Green になることを確認する**

**チェックポイント**: US1 単独で動作確認可能 → `pytest tests/presentation/test_employees.py` が US1 テストで Green

---

## Phase 4: US2 - エラーハンドリング（優先度: P2）

**目標**: 存在しないIDまたは退職済み社員のIDを指定した場合に 404 を返す

**独立テスト**: 存在しないIDと退職済み社員のIDで `GET /api/employees/<id>` をリクエストし、いずれも 404 と `{"error": "社員が見つかりません"}` が返ることを確認する

### US2 のテスト（TDD: 先に書いて Red を確認）

- [X] T010 [US2] test_存在しないIDを指定した場合 404 と `{"error": "社員が見つかりません"}` が返る テストを tests/presentation/test_employees.py に追記し、**Red を確認する**
- [X] T011 [P] [US2] test_退職済み社員のIDを指定した場合 404 が返る テストを tests/presentation/test_employees.py に追記し、**Red を確認する**

### US2 の実装（テスト Green を目指す）

- [X] T012 [US2] app/api/presentation/employees.py の詳細エンドポイントに None チェックと 404 レスポンス `{"error": "社員が見つかりません"}` を実装し、T010・T011 のテストが **Green になることを確認する**

**チェックポイント**: US1・US2 ともに独立して動作確認可能

---

## Phase 5: Polish（仕上げ）

**目的**: コード品質確認と最終検証

- [X] T013 [P] docker compose exec app ruff check . を実行し静的解析エラーがないことを確認する
- [X] T014 docker compose exec app pytest tests/presentation/test_employees.py -v を実行し全テストが Green であることを確認する

---

## 依存関係と実行順序

### フェーズ依存

- **Setup（Phase 1）**: 依存なし・即開始可能
- **Foundational（Phase 2）**: Setup 完了後（T002・T003 は並列実行可）
- **US1（Phase 3）**: Foundational 完了後。テスト（T004〜T006）→ 実装（T007〜T009）の順
- **US2（Phase 4）**: US1 の実装（T007〜T009）完了後。テスト（T010〜T011）→ 実装（T012）の順
- **Polish（Phase 5）**: US2 完了後

### ユーザーストーリー依存

- **US1（P1）**: Foundational 完了後に開始可能・単独でテスト可能
- **US2（P2）**: US1 の実装完了後に開始（エンドポイントが存在することが前提）

### 各ストーリー内の順序

```
テストを書く（Red 確認） → 実装する（Green 確認）
```

### 並列実行可能なタスク

- T002・T003: 同時実行可（異なるファイルの確認）
- T005・T006: T004 の後に同時実行可
- T010・T011: 同時実行可
- T013・T014: T013 は T014 と並列可（ただし T014 は T013 の修正適用後が望ましい）

---

## 並列実行例: US1 のテスト

```bash
# US1 の複数テストを同時追記（別々のテスト関数）:
Task: "test_詳細レスポンスに必要なフィールドが含まれる (T005)"
Task: "test_statusフィールドがレスポンスに含まれない (T006)"
```

---

## 実装戦略

### MVP（US1 のみ）

1. Phase 1・2: Setup・Foundational 確認
2. Phase 3: US1 テスト（Red）→ 実装（Green）
3. **停止して検証**: `GET /api/employees/1` が動作することを確認
4. US1 のみでデプロイ・デモ可能

### 段階的デリバリー

1. Setup + Foundational 確認 → 基盤準備完了
2. US1 追加 → 詳細取得が動作 → デプロイ・デモ（MVP）
3. US2 追加 → エラーハンドリング完成 → デプロイ・デモ
4. Polish → 全テスト Green・静的解析クリア

---

## 備考

- [P] タスク = 異なるファイル、依存なし
- [Story] ラベル = ユーザーストーリーとのトレーサビリティ
- **Red 確認は省略不可**（TDD 大前提）
- 各タスク完了後にチェックボックスを [X] にマークする
- quickstart.md のシナリオを最終確認に使用する
