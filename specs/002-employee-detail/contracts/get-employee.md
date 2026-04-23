# API コントラクト: 社員詳細取得

## エンドポイント

```
GET /api/employees/<id>
```

## リクエスト

### パスパラメータ

| パラメータ | 型 | 必須 | 説明 |
|---|---|---|---|
| id | integer | ✅ | 取得したい社員のID |

### リクエストボディ

なし

---

## レスポンス

### 成功（200 OK）

在籍中の社員が見つかった場合。

```json
{
  "id": 1,
  "name": "山田太郎",
  "role": "エンジニア",
  "position": "主任",
  "department": "開発部",
  "age": 32,
  "hire_date": "2021-04-01",
  "years_of_service": 5
}
```

| フィールド | 型 | 説明 |
|---|---|---|
| id | integer | 社員ID |
| name | string | 氏名 |
| role | string | 役割 |
| position | string | 役職 |
| department | string | 部署 |
| age | integer | 年齢 |
| hire_date | string | 入社日（YYYY-MM-DD） |
| years_of_service | integer | 勤続年数（端数切り捨て） |

**注意**: `status` フィールドはレスポンスに含めない。

---

### エラー（404 Not Found）

以下の場合に返す：
- 指定したIDの社員が存在しない
- 指定したIDの社員のstatusが「退職済」

```json
{
  "error": "社員が見つかりません"
}
```

---

## テストケース

| ケース | 入力 | 期待するステータス | 期待するレスポンス |
|---|---|---|---|
| 正常系: 在籍中社員 | id=1（在籍中） | 200 | 社員情報オブジェクト |
| 異常系: 存在しないID | id=9999 | 404 | `{"error": "社員が見つかりません"}` |
| 異常系: 退職済社員 | id=2（退職済） | 404 | `{"error": "社員が見つかりません"}` |
| 異常系: 文字列ID | id="abc" | 404 | Flask自動処理 |
