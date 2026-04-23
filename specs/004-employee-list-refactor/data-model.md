# Data Model: 社員一覧リファクタリング

**Feature**: Constitution v1.1.0 原則 V 準拠
**Date**: 2026-04-22

## エンティティ: Employee（変更あり）

`domain/repository/employee_repository.py` に移動し、`@dataclass` に変換する。

| フィールド | 型 | 変更 | 説明 |
|---|---|---|---|
| id | int | 型アノテーション追加 | 社員 ID |
| name | str | 型アノテーション追加 | 氏名 |
| role | str | 型アノテーション追加 | 役職 |
| position | str | 型アノテーション追加 | 職位 |
| department | str | 型アノテーション追加 | 部署 |
| age | int | 型アノテーション追加 | 年齢 |
| hire_date | str | 型アノテーション追加 | 入社日（YYYY-MM-DD） |
| years_of_service | int | 変更なし（@property） | 勤続年数（計算値） |

`to_dict()` メソッドは変更なし。

## インターフェース: IEmployeeRepository

`domain/repository/employee_repository.py` に `Employee` と同居。

| メソッド | シグネチャ | 説明 |
|---|---|---|
| `find_all` | `() -> list[Employee]` | 在籍中全社員取得 |
| `find_by_id` | `(employee_id: int) -> Employee \| None` | ID指定・在籍中社員取得 |

## 具象実装: SQLiteEmployeeRepository

`infrastructure/repository/employee_repository.py` に配置。`IEmployeeRepository` を継承。

| メソッド | 実装内容 |
|---|---|
| `find_all` | 既存 `find_active_employees` の SQL を流用 |
| `find_by_id` | 既存 `find_active_employee_by_id` の SQL を流用 |

## DI バインディング

`app/module.py` の `AppModule`:

| インターフェース | 具象実装 |
|---|---|
| `IEmployeeRepository` | `SQLiteEmployeeRepository` |

## 削除対象

| ファイル | 理由 |
|---|---|
| `app/api/domain/employee.py` | `domain/repository/employee_repository.py` に移動 |
| `app/api/infrastructure/employee_repository.py` | `infrastructure/repository/employee_repository.py` に移動 |
