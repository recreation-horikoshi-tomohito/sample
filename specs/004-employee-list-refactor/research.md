# Research: 社員一覧リファクタリング

**Feature**: 社員一覧/詳細を Constitution v1.1.0 原則 V に準拠させる
**Date**: 2026-04-22

## NEEDS CLARIFICATION 解決結果

技術スタックは確定済み。調査項目は flask-injector の利用パターンのみ。

## 技術決定事項

### flask-injector のバージョンと Flask 3.x 互換性

- **Decision**: `flask-injector` を使用する。Flask 3.1 との互換性は 0.15.0 以降で確認済み
- **Rationale**: 原則 V が flask-injector を明示。Flask 3.x の `@inject` サポートあり
- **Alternatives**: `injector` 単体での手動 DI は可能だが原則 V に反する

### @inject をルート関数に付与する方法

- **Decision**: `@employees_bp.route(...)` の直後に `@inject` を付与する（順序重要）
- **Rationale**: flask-injector は Blueprint に対応しており、FlaskInjector 初期化後はルート関数の引数を型アノテーションで解決する
- **Alternatives**: クラスベース View（MethodView）は不要。シンプリシティ原則維持

### SQLiteEmployeeRepository の Flask アプリへのアクセス

- **Decision**: `current_app._get_current_object()` を使う（infrastructure は Flask 依存 OK）
- **Rationale**: リクエストコンテキスト内で `current_app` は常に有効。DI で `app` 自体を渡す必要がない
- **Alternatives**: `app` を直接 inject することも可能だが、`current_app` の方がシンプル

### Employee エンティティの @dataclass 変換

- **Decision**: `@dataclass` に変換し、`@property`（`years_of_service`）と `to_dict()` はそのまま維持
- **Rationale**: `@dataclass` は `@property` と通常メソッドを持てる。既存の `to_dict()` との互換性を保てる
- **Alternatives**: plain class のままにする案は原則 V の `@dataclass` 要件に反する

### 既存テストとの互換性

- **Decision**: `conftest.py`・`test_employees.py` は変更不要
- **Rationale**: `seed()` は `get_db(app)` を直接呼ぶため影響なし。`conftest.py` は `create_app()` を呼ぶだけで FlaskInjector 初期化も内部で完結する
- **Alternatives**: テスト用 Module（モック差し替え）は US2 テスト追加時に対応
