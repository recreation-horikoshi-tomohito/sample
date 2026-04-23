# Quickstart: 社員一覧リファクタリング

**Date**: 2026-04-22

## 動作確認手順

### 前提

```bash
docker compose up -d
```

### テスト実行（外部動作維持の確認）

```bash
# 既存テストがすべてパスすることを確認
docker compose exec app pytest tests/presentation/test_employees.py -v
```

全テストが PASSED となれば US1（外部動作維持）が満たされている。

### 社員一覧 API の手動確認

```bash
# 1. 社員一覧取得（空のとき）
curl -s http://localhost:8081/api/employees | jq .
# → []

# 2. DB に直接データを挿入後
curl -s http://localhost:8081/api/employees | jq .
# → リファクタリング前と同じフォーマットでレスポンス
```

### DI の差し替え確認（US2）

`app/module.py` の `AppModule` でバインディングを変更することで実装を差し替え可能。

```python
# テスト用モジュールの例（テスト内で使用）
class TestModule(Module):
    def configure(self, binder):
        binder.bind(IEmployeeRepository, to=FakeEmployeeRepository)
```

### ruff（静的解析）

```bash
docker compose exec app ruff check .
```

リファクタリング後もエラーなしであることを確認。
