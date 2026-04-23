# Feature Specification: リポジトリ層・ユースケース層テスト追加 + SQLAlchemy移行

**Feature Branch**: `feature/005-repository-tests`  
**Created**: 2026-04-23  
**Status**: Clarified  
**Input**: User description: "リポジトリのテスト追加して"（後にユースケーステスト追加・SQLAlchemy移行を含む範囲に拡張）

## Clarifications

### Session 2026-04-23

- Q: ユースケーステストの検証方式は？ → A: 実DBを使ったインテグレーションテスト
- Q: ユースケーステストで重点的に検証したい内容は？ → A: Entity→EmployeeOutput全フィールドマッピング・years_of_service計算・None返却 全て
- Q: 既存のモックベースのユースケーステストはどうするか？ → A: 削除して新しい実DBインテグレーションテストに置き換える
- Q: SQLAlchemyの適用範囲は？ → A: SQLiteEmployeeRepositoryの実装＋テストfixture両方をSQLAlchemyに移行
- Q: SQLAlchemyのスタイルは？ → A: ORM（DeclarativeBase + EmployeeModelクラス定義）

## User Scenarios & Testing *(mandatory)*

### User Story 1 - リポジトリの正常系テスト (Priority: P1)

開発者が `IEmployeeRepository` の具象実装に対して、データの読み取り操作が正しく機能することをテストで確認できる。

**Why this priority**: リポジトリはデータアクセスの境界であり、データが正しく取得できることを保証することで、上位層（usecase・presentation）の信頼性が担保される。

**Independent Test**: リポジトリテストを実行するだけで、在籍中社員の一覧取得・ID指定取得が正常に動作することを確認できる。

**Acceptance Scenarios**:

1. **Given** 在籍中の社員が複数名DBに登録されている, **When** 全社員取得操作を行う, **Then** 在籍中の社員のみが全員返される
2. **Given** 在籍中の社員がDBに登録されている, **When** その社員のIDを指定して取得する, **Then** 該当社員のデータが返される
3. **Given** 社員が一人もDBに登録されていない, **When** 全社員取得操作を行う, **Then** 空のリストが返される

---

### User Story 2 - リポジトリの異常系テスト (Priority: P2)

開発者が、存在しないデータや対象外のデータに対するリポジトリの振る舞いをテストで確認できる。

**Why this priority**: 正常系が通っても異常系の振る舞いが保証されなければ、本番障害の原因となる。エラーケースを明示的にテストすることで、設計の正確性を担保する。

**Independent Test**: 存在しないIDや退職済み社員を操作したとき、期待する結果（`None` や空リスト）が返ることをテストで確認できる。

**Acceptance Scenarios**:

1. **Given** 退職済みの社員がDBに登録されている, **When** 全社員取得操作を行う, **Then** その社員は結果に含まれない
2. **Given** DBに存在しないIDを指定する, **When** ID指定取得操作を行う, **Then** 結果が `None` として返される
3. **Given** 退職済みの社員のIDを指定する, **When** ID指定取得操作を行う, **Then** 結果が `None` として返される

---

### User Story 3 - ユースケース層インテグレーションテスト (Priority: P2)

開発者が `FindEmployeeListUseCase` および `FindEmployeeDetailUseCase` に対して、実DBを使ったインテグレーションテストでビジネスロジックを検証できる。

**Why this priority**: ユースケース層はEntity→EmployeeOutput変換と勤続年数計算を担う。リポジトリテストだけでは層を跨いだ変換ロジックの正確性が保証されないため、ユースケース単位の検証が必要。

**Independent Test**: ユースケーステストを実行するだけで、Entity→EmployeeOutput変換・years_of_service計算・None返却が正しく動作することを確認できる。

**Acceptance Scenarios**:

1. **Given** 在籍中社員がDBに存在する, **When** `FindEmployeeListUseCase.execute()` を呼ぶ, **Then** `EmployeeOutput` のリストが返され全フィールドが正確にマッピングされている
2. **Given** hire_dateが既知の在籍中社員がDBに存在する, **When** `FindEmployeeListUseCase.execute()` を呼ぶ, **Then** `years_of_service` が正確に計算されている
3. **Given** 在籍中社員がDBに存在する, **When** `FindEmployeeDetailUseCase.execute(id)` を呼ぶ, **Then** 該当社員の `EmployeeOutput` が返される
4. **Given** 存在しないIDを指定する, **When** `FindEmployeeDetailUseCase.execute(id)` を呼ぶ, **Then** `None` が返される
5. **Given** 退職済み社員のIDを指定する, **When** `FindEmployeeDetailUseCase.execute(id)` を呼ぶ, **Then** `None` が返される

---

### User Story 4 - SQLAlchemy ORM移行 (Priority: P1)

開発者が `SQLiteEmployeeRepository` の実装をSQLAlchemy ORM（DeclarativeBase）ベースに移行し、テストfixture（seeding）もSQLAlchemy sessionを通じて行える。

**Why this priority**: テストと実装の一貫性を保つため。SQLAlchemyを導入することでテストのseeding・クエリが統一され、将来的なDB移行への耐性も上がる。

**Acceptance Scenarios**:

1. **Given** SQLAlchemy `EmployeeModel`（DeclarativeBase継承）が定義されている, **When** リポジトリが `EmployeeModel` 経由でクエリを実行する, **Then** 正しいEmployeeエンティティが返される
2. **Given** テストfixture が SQLAlchemy session経由でデータをseedする, **When** テストを実行する, **Then** テスト間でDBが独立しており干渉が発生しない

---

### Edge Cases

- DBに同一IDの社員が重複登録されている場合はどうなるか（DBの一意制約で防がれる想定）
- ステータスが `在籍中` でも `退職済` でもない値の場合、取得結果に含まれないことを確認する

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: リポジトリの全件取得操作は、ステータスが在籍中の社員のみを返さなければならない（MUST）
- **FR-002**: リポジトリのID指定取得操作は、該当IDの在籍中社員を返さなければならない（MUST）
- **FR-003**: リポジトリのID指定取得操作は、対象が存在しない場合 `None` を返さなければならない（MUST）
- **FR-004**: リポジトリのID指定取得操作は、対象が退職済みの場合 `None` を返さなければならない（MUST）
- **FR-005**: 各テストは独立した状態のDBを使用し、テスト間で干渉してはならない（MUST）
- **FR-006**: テストはモックを使用せず、実DBへのアクセスを通じて検証しなければならない（MUST）
- **FR-007**: `FindEmployeeListUseCase` のインテグレーションテストは、全フィールドのマッピング正確性・勤続年数計算を実DBで検証しなければならない（MUST）
- **FR-008**: `FindEmployeeDetailUseCase` のインテグレーションテストは、正常取得・存在しないID・退職済みIDの全ケースを実DBで検証しなければならない（MUST）
- **FR-009**: `tests/presentation/test_employees.py` 内の既存モックベースユースケーステスト（`FakeEmployeeRepository`を使った3件）は削除し、新しい実DBテストに置き換えなければならない（MUST）
- **FR-010**: `SQLiteEmployeeRepository` の実装はSQLAlchemy ORM（`DeclarativeBase` + `EmployeeModel`）に移行しなければならない（MUST）
- **FR-011**: テストfixture（seeding）はSQLAlchemy sessionを通じて行わなければならない（MUST）

### Key Entities

- **Employee**: 社員ドメインエンティティ（id, name, role, position, department, age, hire_date を持つ）
- **EmployeeModel**: SQLAlchemy ORMモデル（infrastructure層、`DeclarativeBase`継承）
- **EmployeeOutput**: usecase→presentation間のDTO（id, name, role, position, department, age, hire_date, years_of_service を持つ）
- **IEmployeeRepository**: リポジトリインターフェース（テスト対象の抽象型）

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: リポジトリの全取得・ID指定取得の正常系・異常系をカバーするテストが全て通過する
- **SC-002**: ユースケース層のインテグレーションテストが全て通過する（マッピング・勤続年数・None返却を含む）
- **SC-003**: 全テストがモック不使用で実DBを操作し、実際の振る舞いを検証している
- **SC-004**: `SQLiteEmployeeRepository`がSQLAlchemy ORM経由でクエリを実行し、既存の全テストが引き続き通過する
- **SC-005**: 新旧全テストスイートを実行して0件の失敗が発生する

## Assumptions

- SQLAlchemy は `DeclarativeBase` スタイル（SQLAlchemy 2.x）を使用する
- テストfixture は SQLAlchemy session経由のseedingに移行する（既存の生SQLite seedは廃止）
- `EmployeeModel` は infrastructure層（`app/api/infrastructure/`）に配置する
- ユースケーステストは `tests/usecase/employee/` 配下に配置する
- リポジトリテストは `tests/infrastructure/repository/` 配下に配置する
- 社員の `status` フィールドは在籍中・退職済みの2種類を想定する
