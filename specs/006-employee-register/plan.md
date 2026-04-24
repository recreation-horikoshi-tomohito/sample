# Implementation Plan: 社員登録機能

**Branch**: `feature/issues-22` | **Date**: 2026-04-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-employee-register/spec.md`

## Summary

`POST /api/employees` エンドポイントを追加し、社員情報をDBに登録する。
TDD（Red→Green→Refactor）サイクルに従い、テストファイルを先に実装する。
既存のクリーンアーキテクチャ・DIパターンを踏襲し、最小限の変更で実現する。

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: Flask 3.1, SQLAlchemy 2.x, injector 0.22.0, pytest 8.3.5, ruff
**Storage**: SQLite
**Testing**: pytest（テストファースト必須）
**Target Platform**: Docker コンテナ（Linux, ポート5000→ホスト8081）
**Project Type**: Web API（REST）
**Performance Goals**: N/A（このスケールでは不要）
**Constraints**: Constitution III - 型アノテーションなし、ロギングなし、YAGNI徹底
**Scale/Scope**: 小規模（既存と同一スタック）

## Constitution Check

| 原則 | チェック項目 | 判定 |
|---|---|---|
| 大前提（TDD） | テストファイルを先に作成し、Red確認後に実装する | ✅ 必須 |
| I. クリーンアーキテクチャ | domain層はFlask/SQLAlchemy非依存 | ✅ 準拠 |
| I. クリーンアーキテクチャ | 層を跨ぐ際はdataclassに変換（EmployeeInput/EmployeeCreateOutput） | ✅ 準拠 |
| I. クリーンアーキテクチャ | usecase層はinfrastructure層をimportしない | ✅ 準拠 |
| II. Blueprintパターン | POST /api/employees は既存 employees.py Blueprint に追加 | ✅ 準拠 |
| II. Blueprintパターン | tests/presentation/test_employees.py にテスト追加 | ✅ 必須 |
| II. Blueprintパターン | エラーレスポンスは400または500のみ | ✅ 準拠 |
| III. シンプリシティ | 型アノテーションなし | ✅ 必須 |
| III. シンプリシティ | ロギングなし | ✅ 必須 |
| III. シンプリシティ | バリデーターライブラリなし（最小限チェックのみ） | ✅ 準拠 |
| IV. 日本語ドキュメント | コメント・ドキュメントは日本語 | ✅ 必須 |
| V. インターフェース分離 | IEmployeeRepository に save() を追加 | ✅ 準拠 |
| V. インターフェース分離 | ICreateEmployeeUseCase インターフェース定義 | ✅ 準拠 |
| V. DI | AppModule に ICreateEmployeeUseCase バインディング追加 | ✅ 必須 |

**Constitution Check 結果**: すべてのゲートを通過。違反なし。

## Project Structure

### Documentation (this feature)

```text
specs/006-employee-register/
├── plan.md              # このファイル
├── research.md          # Phase 0 出力（完了）
├── data-model.md        # Phase 1 出力（完了）
├── quickstart.md        # Phase 1 出力（完了）
├── contracts/
│   └── post_employees.md  # Phase 1 出力（完了）
├── checklists/
│   └── requirements.md
└── tasks.md             # /speckit-tasks で生成
```

### Source Code（変更対象ファイル）

```text
app/
└── api/
    ├── core/
    │   ├── domain/
    │   │   ├── employee/
    │   │   │   └── __init__.py          # EmployeeCreateOutput dataclass 追加
    │   │   └── repository/
    │   │       └── employee_repository.py  # save() メソッド追加
    │   └── usecase/
    │       └── employee/
    │           ├── __init__.py           # ICreateEmployeeUseCase インターフェース追加
    │           └── create_employee.py   # CreateEmployeeUseCase 具象実装（新規）
    ├── infrastructure/
    │   └── repository/
    │       └── employee_repository.py   # save() 具象実装追加
    └── presentation/
        └── employees.py                 # POST /api/employees ルート追加
└── module.py                            # ICreateEmployeeUseCase バインディング追加

tests/
├── core/
│   └── usecase/
│       └── employee/
│           └── test_create_employee.py  # ユースケーステスト（新規）
└── presentation/
    └── test_employees.py                # POST テスト追加
```

### 実装の依存関係

```
EmployeeCreateOutput（domain/__init__.py）
  ↓
IEmployeeRepository.save()（domain/repository/）
  ↓
SQLiteEmployeeRepository.save()（infrastructure/repository/）
  ↓
ICreateEmployeeUseCase（usecase/employee/__init__.py）
  ↓
CreateEmployeeUseCase（usecase/employee/create_employee.py）
  ↓
AppModule バインディング（app/module.py）
  ↓
POST /api/employees ルート（presentation/employees.py）
```

### バリデーション設計（presentation層）

```python
# 必須フィールドの確認
REQUIRED_FIELDS = ["name", "role", "position", "department", "age", "hire_date"]

# 型・値のチェック
# - age: int かつ >= 0
# - hire_date: YYYY-MM-DD形式（正規表現または strptime）
# - name: 空文字不可

# エラーレスポンス形式（既存パターンと統一）
{"error": "必須フィールドが不足しています"}
```

## Complexity Tracking

Constitution違反なし。複雑性追跡不要。
