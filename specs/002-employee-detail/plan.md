# 実装計画: 社員詳細機能

**ブランチ**: `feature/issues-10` | **作成日**: 2026-04-20 | **Spec**: [spec.md](spec.md)

## サマリー

社員IDを指定して在籍中社員の詳細情報を返す `GET /api/employees/<id>` エンドポイントを実装する。
既存のオニオンアーキテクチャ・employeesリソース構成を拡張する形で、リポジトリ・ユースケース・Blueprintを追加する。

## 技術コンテキスト

**言語/バージョン**: Python 3.12
**主要依存**: Flask 3.1、uv（パッケージ管理）、ruff（静的解析）
**ストレージ**: SQLite（raw sqlite3、ORMなし）
**テスト**: pytest、tempfile.mkstemp によるテスト毎の独立DBファイル
**ターゲットプラットフォーム**: Docker コンテナ（Linux）
**プロジェクト種別**: web-service（REST API）
**パフォーマンス目標**: 標準的なWebアプリ水準
**制約**: 型アノテーションなし・ロギングなし・シンプリシティ厳守

## Constitution Check

| 原則 | 確認 | 備考 |
|---|---|---|
| 大前提: TDD | ✅ | テスト先行（Red確認後にGreen） |
| I. オニオンアーキテクチャ | ✅ | `presentation → usecase → domain` 維持 |
| II. Blueprintパターン | ✅ | 既存 `employees.py` に追加（同リソース） |
| III. シンプリシティ | ✅ | 型アノテーションなし・ロギングなし |
| IV. 日本語ドキュメント | ✅ | 全ドキュメント日本語 |

## プロジェクト構成

### ドキュメント（本フィーチャー）

```text
specs/002-employee-detail/
├── plan.md              ← 本ファイル
├── spec.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── get-employee.md
└── tasks.md             ← /speckit-tasks で生成
```

### ソースコード変更箇所

```text
app/
└── api/
    ├── domain/
    │   └── employee.py                  # 変更なし
    ├── usecase/
    │   ├── get_employees.py             # 変更なし
    │   └── get_employee.py              # 新規: get_employee(app, id)
    ├── infrastructure/
    │   ├── database.py                  # 変更なし
    │   └── employee_repository.py       # 追加: find_active_employee_by_id(app, id)
    └── presentation/
        └── employees.py                 # 追加: GET /api/employees/<int:id>

tests/
└── presentation/
    └── test_employees.py                # 追加: 社員詳細のテストケース
```

## 実装方針

### リポジトリ層

`find_active_employee_by_id(app, id)` を `employee_repository.py` に追加。

```python
def find_active_employee_by_id(app, employee_id):
    db = get_db(app)
    row = db.execute(
        "SELECT id, name, role, position, department, age, hire_date"
        " FROM employees WHERE id = ? AND status = '在籍中'",
        (employee_id,)
    ).fetchone()
    if row is None:
        return None
    return Employee(**dict(row))
```

### ユースケース層

`get_employee.py` を新規作成。

```python
from app.api.infrastructure.employee_repository import find_active_employee_by_id

def get_employee(app, employee_id):
    employee = find_active_employee_by_id(app, employee_id)
    if employee is None:
        return None
    return employee.to_dict()
```

### プレゼンテーション層

`employees.py` に詳細エンドポイントを追加。

```python
@employees_bp.route("/api/employees/<int:employee_id>")
def get_employee_detail(employee_id):
    employee = get_employee_usecase(current_app._get_current_object(), employee_id)
    if employee is None:
        return jsonify({"error": "社員が見つかりません"}), 404
    return jsonify(employee)
```

## Complexity Tracking

違反なし。
