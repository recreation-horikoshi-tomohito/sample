# sample Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-20

## Active Technologies

- Python 3.12 + Flask 3.1、uv（パッケージ管理）、ruff（静的解析・フォーマット） (develop)

## Project Structure

```text
app/
└── api/
    ├── domain/          # エンティティ・ビジネスロジック（最内層）
    ├── usecase/         # ユースケース
    ├── infrastructure/  # 外部依存（SQLite等）
    └── presentation/    # FlaskのBlueprint（最外層）
tests/
└── presentation/        # Blueprintファイルに対応するテストファイル
```

依存方向: `presentation → usecase → domain`（内側に向かってのみ依存）

## Commands

```bash
# コンテナ起動
docker compose up -d

# テスト実行（コンテナ内）
docker compose exec app pytest -v

# 静的解析
docker compose exec app ruff check .
```

## Code Style

Python 3.12: Follow standard conventions

## Recent Changes

- develop: Added Python 3.12 + Flask 3.1、uv（パッケージ管理）、ruff（静的解析・フォーマット）

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
