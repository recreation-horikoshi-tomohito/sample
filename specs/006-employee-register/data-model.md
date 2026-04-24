# Data Model: 社員登録機能

**Feature**: 社員登録機能（#22）
**Date**: 2026-04-24

## エンティティ

### Employee（社員エンティティ）

既存エンティティ。変更なし。

| フィールド | 型 | 制約 | 説明 |
|---|---|---|---|
| id | int | PK, 自動採番 | 社員ID |
| name | str | NOT NULL | 氏名 |
| role | str | NOT NULL | 役割 |
| position | str | NOT NULL | 役職 |
| department | str | NOT NULL | 部署 |
| age | int | NOT NULL | 年齢 |
| hire_date | str | NOT NULL, YYYY-MM-DD | 入社日 |

`years_of_service` はプロパティ（計算値）であり永続化フィールドではない。

### EmployeeModel（ORM モデル）

既存モデル。変更なし。

`status` カラムを持つ（CHECK 制約: `在籍中` または `退職済`、デフォルト: `在籍中`）。

---

## DTO（データ転送オブジェクト）

### EmployeeInput（既存・変更なし）

登録リクエストの入力DTO。`domain/employee/__init__.py` に定義済み。

| フィールド | 型 | 説明 |
|---|---|---|
| name | str | 氏名 |
| role | str | 役割 |
| position | str | 役職 |
| department | str | 部署 |
| age | int | 年齢 |
| hire_date | str | 入社日（YYYY-MM-DD） |

`status` は含まない（登録時は常に「在籍中」固定のため）。

### EmployeeCreateOutput（新規追加）

登録成功時のレスポンスDTO。`domain/employee/__init__.py` に追加する。

| フィールド | 型 | 説明 |
|---|---|---|
| id | int | 採番された社員ID |
| name | str | 氏名 |
| role | str | 役割 |
| position | str | 役職 |
| department | str | 部署 |
| age | int | 年齢 |
| hire_date | str | 入社日（YYYY-MM-DD） |
| status | str | 在籍状態（常に「在籍中」） |

`years_of_service` は含まない（登録直後は不要・YAGNI）。

---

## バリデーションルール

| フィールド | ルール | エラー |
|---|---|---|
| name | 空文字・欠落は不可 | 400 |
| role | 欠落は不可 | 400 |
| position | 欠落は不可 | 400 |
| department | 欠落は不可 | 400 |
| age | 欠落・非整数・負の値は不可 | 400 |
| hire_date | 欠落・YYYY-MM-DD形式以外は不可 | 400 |

---

## リポジトリインターフェース変更

`IEmployeeRepository` に以下を追加:

```
save(input: EmployeeInput) -> Employee
```

- 入力: `EmployeeInput`（DTOから直接受け取る）
- 出力: 永続化後の `Employee` エンティティ（idが採番済み）
- `status` は infrastructure層で「在籍中」を設定する
