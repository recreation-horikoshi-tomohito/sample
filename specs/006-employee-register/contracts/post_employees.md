# Contract: POST /api/employees

**Feature**: 社員登録機能（#22）
**Date**: 2026-04-24

## エンドポイント

```
POST /api/employees
Content-Type: application/json
```

---

## リクエスト

### ボディ（JSON）

```json
{
  "name": "山田 太郎",
  "role": "エンジニア",
  "position": "主任",
  "department": "開発部",
  "age": 30,
  "hire_date": "2020-04-01"
}
```

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| name | string | ✓ | 氏名（空文字不可） |
| role | string | ✓ | 役割 |
| position | string | ✓ | 役職 |
| department | string | ✓ | 部署 |
| age | integer | ✓ | 年齢（正の整数） |
| hire_date | string | ✓ | 入社日（YYYY-MM-DD形式） |

---

## レスポンス

### 201 Created（成功）

```json
{
  "id": 1,
  "name": "山田 太郎",
  "role": "エンジニア",
  "position": "主任",
  "department": "開発部",
  "age": 30,
  "hire_date": "2020-04-01",
  "status": "在籍中"
}
```

### 400 Bad Request（クライアントエラー）

必須フィールド欠落・型不正・フォーマット違反の場合。

```json
{
  "error": "必須フィールドが不足しています"
}
```

### 500 Internal Server Error（サーバーエラー）

DB障害等、サーバー内部の問題。

```json
{
  "error": "サーバーエラーが発生しました"
}
```

---

## ビジネスルール

- `status` はリクエストで指定不可。常に「在籍中」で登録される
- 同名社員の重複登録は禁止しない
- `age` に負の値は不可（400）
- `hire_date` の未来日付は許容する
