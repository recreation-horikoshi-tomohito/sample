# 社員管理 API

Flask + SQLAlchemy で構築した社員管理 REST API。クリーンアーキテクチャに基づき設計。

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| 言語 | Python 3.12 |
| フレームワーク | Flask 3.1 |
| ORM | SQLAlchemy 2.x |
| DI | injector 0.22.0 |
| テスト | pytest 8.3.5 |
| Lint | ruff |
| DB | SQLite |
| コンテナ | Docker |

## セットアップ

```bash
docker compose up -d
```

`http://localhost:8081` でアクセス可能。

## API

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/employees` | 在籍中社員一覧を取得 |
| GET | `/employees/:id` | 社員詳細を取得 |

## テスト・Lint

```bash
# テスト実行
docker compose exec app-container pytest -v

# Lint
docker compose exec app-container ruff check .
```

## アーキテクチャ

クリーンアーキテクチャに基づき、依存方向は内側（domain）のみに向かう。

```
app/api/
├── core/
│   ├── domain/        # エンティティ・リポジトリインターフェース
│   └── usecase/       # ユースケース（シングルアクション）
├── infrastructure/    # SQLAlchemy ORM・具象実装
└── presentation/      # Flask Blueprint
```

## Claude Code セキュリティ設定

このプロジェクトは Claude Code 向けのセキュリティ設定（`.claude/settings.json`）を含む。
設定の確認・セットアップには以下のチェックリストを参照。

🔐 [Claude Code セキュリティチェックリスト](https://recreation-horikoshi-tomohito.github.io/sample/.claude/checklist.html)
