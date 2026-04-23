# クイックスタート: 社員詳細機能

**フィーチャー**: 社員詳細機能（#10）
**作成日**: 2026-04-20

## 統合テストシナリオ

### シナリオ 1: 在籍中社員の詳細取得（正常系）

```
前提: 在籍中の社員（id=1, name="山田太郎"）がDBに存在する
操作: GET /api/employees/1
期待: 200 OK、社員詳細JSONが返る（statusフィールドなし）
```

### シナリオ 2: 存在しないIDへのリクエスト（異常系）

```
前提: id=9999 の社員はDBに存在しない
操作: GET /api/employees/9999
期待: 404、{"error": "社員が見つかりません"}
```

### シナリオ 3: 退職済社員へのリクエスト（異常系）

```
前提: 退職済の社員（id=2, status="退職済"）がDBに存在する
操作: GET /api/employees/2
期待: 404、{"error": "社員が見つかりません"}
```

### シナリオ 4: 複数社員から正しい1名を取得

```
前提: 在籍中の社員が複数DBに存在する
操作: GET /api/employees/<特定のid>
期待: 200 OK、指定したIDの社員のみのデータが返る
```

## 実装後の確認手順

```bash
# コンテナ起動
docker compose up -d

# 正常系確認
curl http://localhost:8081/api/employees/1

# 存在しないID確認
curl -i http://localhost:8081/api/employees/9999

# テスト一括実行
docker compose exec app pytest tests/presentation/test_employees.py -v
```
