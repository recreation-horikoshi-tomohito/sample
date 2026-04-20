# APIコントラクト: 社員一覧取得

**エンドポイント**: `GET /api/employees`
**作成日**: 2026-04-20

## 概要

在籍中の全社員の情報をJSON形式で返す。退職済の社員は含まれない。

## リクエスト

```
GET /api/employees
```

**ヘッダー**: 特になし（認証は本スコープ外）
**クエリパラメータ**: なし
**リクエストボディ**: なし

## レスポンス

### 200 OK — 正常取得

```json
[
  {
    "id": 1,
    "name": "山田 太郎",
    "role": "エンジニア",
    "position": "主任",
    "department": "開発部",
    "age": 32,
    "hire_date": "2021-04-01",
    "years_of_service": 5
  },
  {
    "id": 2,
    "name": "鈴木 花子",
    "role": "デザイナー",
    "position": "一般",
    "department": "デザイン部",
    "age": 27,
    "hire_date": "2024-10-01",
    "years_of_service": 1
  }
]
```

### 200 OK — 在籍中の社員が0名の場合

```json
[]
```

### 500 Internal Server Error — サーバーエラー

```json
{
  "error": "Internal Server Error"
}
```

## フィールド定義

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `id` | integer | 社員ID |
| `name` | string | 氏名 |
| `role` | string | 役割 |
| `position` | string | 役職 |
| `department` | string | 部署名 |
| `age` | integer | 年齢 |
| `hire_date` | string | 入社日（YYYY-MM-DD形式） |
| `years_of_service` | integer | 勤続年数（入社日から現在日付を元に計算、年単位切り捨て） |

## 制約・注意事項

- `status = '退職済'` の社員はレスポンスに含まれない
- `years_of_service` はDBに保存せず、レスポンス生成時に計算する
- レスポンスの並び順はDB登録順（保証なし）
