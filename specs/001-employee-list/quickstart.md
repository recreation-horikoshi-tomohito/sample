# クイックスタート: 社員一覧機能

**機能**: 社員一覧取得API
**作成日**: 2026-04-20

## 前提条件

- Docker・docker compose がインストール済み
- リポジトリのルートディレクトリにいること

## 起動手順

```bash
# コンテナを起動
docker compose up -d

# 起動確認
docker compose ps
```

アクセス先: `http://localhost:8081`

## 社員一覧APIの動作確認

### 全件取得

```bash
curl http://localhost:8081/api/employees
```

**期待されるレスポンス（社員が登録されている場合）**:

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
  }
]
```

**期待されるレスポンス（在籍中の社員が0名の場合）**:

```json
[]
```

## テストの実行

```bash
# コンテナ内でテスト実行
docker compose exec app pytest tests/presentation/test_employees.py -v

# 全テスト実行
docker compose exec app pytest -v
```

## 動作検証チェックリスト

- [ ] `GET /api/employees` が200で返る
- [ ] 在籍中の社員のみがレスポンスに含まれる（退職済は除外）
- [ ] 各社員に `years_of_service` が正しく計算されて返される
- [ ] 在籍中の社員が0名の場合に空配列 `[]` が返される
- [ ] テストがすべてパスする
