# Feature Specification: 社員登録機能

**Feature Branch**: `feature/issues-22`
**Created**: 2026-04-24
**Status**: Draft
**Input**: User description: "#22 で社員登録機能を実装する"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 社員情報を登録する (Priority: P1)

管理者が新しい社員の情報を登録する。必要な情報（氏名・役職・部署・年齢・入社日など）をリクエストとして送信すると、システムが社員データを永続化し、登録結果を返す。

**Why this priority**: 社員登録はこの機能の唯一のユースケースであり、すべての価値を提供する中核。

**Independent Test**: `POST /employees` にJSONボディを送信し、正常な登録レスポンスが返ることを確認するだけで完結する。

**Acceptance Scenarios**:

1. **Given** 必須フィールド（name, role, position, department, age, hire_date）が揃ったリクエスト、**When** `POST /employees` を呼ぶ、**Then** 201レスポンスと登録された社員情報（id含む）のJSONが返る
2. **Given** 必須フィールドが不足したリクエスト、**When** `POST /employees` を呼ぶ、**Then** 400レスポンスとエラーの説明メッセージが返る
3. **Given** DBが使用不能な状態、**When** `POST /employees` を呼ぶ、**Then** 500レスポンスが返る

---

### Edge Cases

- `age` に負の値や文字列が渡された場合は400エラーを返す
- `hire_date` がISO 8601形式（YYYY-MM-DD）でない場合は400エラーを返す
- `name` が空文字の場合は400エラーを返す
- 登録時の `status` は常に「在籍中」（クライアントから指定不可）

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: システムは `POST /employees` エンドポイントを提供しなければならない（MUST）
- **FR-002**: リクエストボディはJSON形式で受け付けなければならない（MUST）
- **FR-003**: リクエストには name, role, position, department, age, hire_date の6フィールドが必須である（MUST）
- **FR-004**: 登録時に `status` は常に「在籍中」で初期化し、クライアントから変更できないようにしなければならない（MUST）
- **FR-005**: 登録成功時は201レスポンスで `EmployeeCreateOutput`（id, name, role, position, department, age, hire_date, status）をJSONで返さなければならない（MUST）
- **FR-006**: 必須フィールド欠落・型不正などクライアント起因のエラーは400レスポンスで返さなければならない（MUST）
- **FR-007**: サーバー内部エラーは500レスポンスで返さなければならない（MUST）
- **FR-008**: ユースケース層はシングルアクションユースケースパターンで実装しなければならない（MUST）
- **FR-009**: 新機能の実装はテスト（Red）を先に書いてから実装（Green）に移行しなければならない（MUST）

### Key Entities

- **Employee（社員）**: id（自動採番）, name（氏名）, role（役割）, position（役職）, department（部署）, age（年齢・整数）, hire_date（入社日・YYYY-MM-DD）, status（在籍状態・デフォルト「在籍中」）
- **EmployeeInput**: 登録リクエストのDTOで、status以外の6フィールドを持つ（dataclass）
- **EmployeeCreateOutput**: 登録完了後のレスポンスDTO（新規dataclass）。フィールド: id, name, role, position, department, age, hire_date, status。`years_of_service` は含まない（登録直後は不要・YAGNI）

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 有効なリクエストに対して、社員がDBに永続化され201レスポンスが返る
- **SC-002**: 必須フィールドが欠けたリクエストに対して、400レスポンスが即座に返る
- **SC-003**: テストが全ケース（正常系・異常系）をカバーし、すべてパスする
- **SC-004**: 既存のGET /employees・GET /employees/:id のテストがすべて引き続きパスする（リグレッションなし）

## Assumptions

- 認証・認可は現時点でスコープ外（全リクエストを受け付ける）
- `age` は整数値で受け取る（生年月日からの計算はしない）
- 同名社員の重複登録は禁止しない（ユニーク制約なし）
- レスポンスフィールドの順序は実装依存とする
- 既存の `EmployeeModel`・`EmployeeInput`・`EmployeeOutput` などのデータ構造を最大限再利用する

## Clarifications

### Session 2026-04-24

- Q: 登録時に status をクライアントが指定できるか？ → A: できない。常に「在籍中」で固定
- Q: 登録成功時のHTTPステータスコードは？ → A: 201 Created
- Q: 登録成功レスポンスのフィールド構成は？ → A: 新規 EmployeeCreateOutput（id, name, role, position, department, age, hire_date, status）を使用。years_of_service は含まない
