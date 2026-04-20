# データモデル: 社員一覧

**機能**: 社員一覧取得API
**作成日**: 2026-04-20

## エンティティ定義

### Employee（社員）

社員を表す中心エンティティ。在籍状況（`status`）でアクティブかどうかを管理する。

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `id` | INTEGER | ✅ | 自動採番の主キー |
| `name` | TEXT | ✅ | 氏名 |
| `role` | TEXT | ✅ | 役割（例: エンジニア、デザイナー、マネージャー） |
| `position` | TEXT | ✅ | 役職（例: 一般、主任、課長、部長） |
| `department` | TEXT | ✅ | 部署名 |
| `age` | INTEGER | ✅ | 年齢 |
| `hire_date` | TEXT | ✅ | 入社日（ISO形式: YYYY-MM-DD） |
| `status` | TEXT | ✅ | 在籍状況（`在籍中` または `退職済`）デフォルト: `在籍中` |

**補足**:
- `years_of_service`（勤続年数）は `hire_date` から現在日付を元にAPIレスポンス時に計算する。DBには保持しない。
- `status = '在籍中'` の社員のみが本APIで返される。`status = '退職済'` の社員は別APIで対応予定。

## DBスキーマ（SQLite）

```sql
CREATE TABLE employees (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    role      TEXT    NOT NULL,
    position  TEXT    NOT NULL,
    department TEXT   NOT NULL,
    age       INTEGER NOT NULL,
    hire_date TEXT    NOT NULL,
    status    TEXT    NOT NULL DEFAULT '在籍中'
                      CHECK (status IN ('在籍中', '退職済'))
);
```

## バリデーションルール

| フィールド | ルール |
|-----------|--------|
| `name` | 空文字不可 |
| `age` | 正の整数 |
| `hire_date` | ISO形式（YYYY-MM-DD）、未来日付不可 |
| `status` | `在籍中` または `退職済` のみ |

## 勤続年数の計算ロジック

```
years_of_service = (現在日付 - hire_date) の年数（端数切り捨て）
```

例:
- `hire_date = 2021-04-01`、現在日付 `2026-04-20` → 勤続年数 `5` 年
- `hire_date = 2026-01-01`、現在日付 `2026-04-20` → 勤続年数 `0` 年
