# データモデル: 社員詳細機能

**フィーチャー**: 社員詳細機能（#10）
**作成日**: 2026-04-20

## エンティティ

### Employee（社員）

既存エンティティ。本機能では変更なし。

| フィールド | 型 | 説明 | レスポンス含有 |
|---|---|---|---|
| id | INTEGER (PK, AUTOINCREMENT) | 社員ID | ✅ |
| name | TEXT NOT NULL | 氏名 | ✅ |
| role | TEXT NOT NULL | 役割 | ✅ |
| position | TEXT NOT NULL | 役職 | ✅ |
| department | TEXT NOT NULL | 部署 | ✅ |
| age | INTEGER NOT NULL | 年齢 | ✅ |
| hire_date | TEXT NOT NULL | 入社日（ISO 8601: YYYY-MM-DD） | ✅ |
| status | TEXT NOT NULL | 在籍状況（'在籍中' / '退職済'） | ❌（フィルタ用のみ） |
| years_of_service | —（計算値） | 勤続年数（端数切り捨て） | ✅ |

### バリデーションルール

- `id`: URL パスパラメータ。Flask `<int:id>` による型変換で非整数は自動的に404
- `status = '在籍中'` の社員のみ取得対象（退職済みは404扱い）

### 状態遷移

本機能では状態変更を行わない（読み取り専用）。

## 既存DBスキーマとの対応

```sql
-- 既存スキーマ（変更なし）
CREATE TABLE IF NOT EXISTS employees (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    role       TEXT NOT NULL,
    position   TEXT NOT NULL,
    department TEXT NOT NULL,
    age        INTEGER NOT NULL,
    hire_date  TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT '在籍中'
               CHECK (status IN ('在籍中', '退職済'))
);
```

DBスキーマへの変更は不要。
