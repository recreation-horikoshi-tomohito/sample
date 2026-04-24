# sample Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-23

## Active Technologies

- Python 3.12 + Flask 3.1、uv（パッケージ管理）、ruff（静的解析・フォーマット） (develop)
- injector 0.22.0（DI） (feature/issues-15)
- SQLAlchemy 2.x（ORM、DeclarativeBase + Column スタイル） (feature/issues-15)

## Project Structure

```text
app/
└── api/
    ├── core/                # ビジネスロジック（最内層）
    │   ├── domain/
    │   │   ├── <概念>/      # 例: employee/
    │   │   │   ├── __init__.py  # @dataclass 値オブジェクト / DTO
    │   │   │   └── <概念>.py    # エンティティ（__init__＋ロジック）
    │   │   └── repository/  # リポジトリインターフェース（IXxx(ABC)）
    │   └── usecase/         # アプリケーションビジネスルール
    ├── infrastructure/      # 外部依存（SQLite / SQLAlchemy ORM）
    │   ├── models/          # SQLAlchemy ORM モデル
    │   └── repository/      # 具象実装
    └── presentation/        # FlaskのBlueprint（最外層）
app/
└── module.py                # AppModule: injectorバインディング定義
tests/
├── core/
│   └── usecase/             # usecase層インテグレーションテスト
├── infrastructure/
│   └── repository/          # リポジトリ層インテグレーションテスト
└── presentation/            # Blueprintファイルに対応するテストファイル
```

アーキテクチャ: クリーンアーキテクチャ（依存方向は内側のみ、ドメインサービスなし）

## Commands

pytest・ruff はサンドボックス環境内で **直接実行する**（`docker compose exec` は使わない）。

```bash
# テスト実行
pytest -v

# 特定ファイル／ディレクトリのみ実行
pytest tests/presentation/ -v

# 静的解析
ruff check .

# フォーマット
ruff format .
```

### TDD サイクル

```bash
# 失敗したテストで即停止（Red → Green の確認に便利）
pytest -v --tb=short -x
```

### pre-commit

コミット前に ruff・pytest が自動実行される（`.pre-commit-config.yaml` で定義）。

devコンテナ初回起動時に `postCreateCommand` で自動セットアップされる。手動で再セットアップする場合:

```bash
pre-commit install
```

## Code Style

Python 3.12: Follow standard conventions

## Recent Changes

- develop: Added Python 3.12 + Flask 3.1、uv（パッケージ管理）、ruff（静的解析・フォーマット）

<!-- MANUAL ADDITIONS START -->

## Security & Sandbox

### なぜサンドボックスが必要か

`deny` ルールだけでは防げないリスクが残る:

| リスク | 例 |
|---|---|
| プロンプトインジェクション | 悪意ある README を読み込んで Claude Code が操作される |
| 予期しないコマンド実行 | コピペしたコードの中に危険なコマンドが混入 |
| 情報の外部送信 | 機密情報を `curl` で外部サーバーに送信される |

サンドボックスは、万が一これらが起きても **被害を箱の中に閉じ込める** 仕組み。

### OS サンドボックスの仕組み

Claude Code の **Bash 実行を OS レベルで隔離する**（`settings.json` の `sandbox` キーで設定）。

**重要**: ファイルシステム・ネットワークの許可制御は `permissions`（Read/Edit/WebFetch）で行う。
`sandbox` の `network.allowedDomains` は Bash とそのサブプロセス（npm, pip, curl など）の通信先を制限する。

| 設定 | 役割 |
|---|---|
| `sandbox.network.allowedDomains` | Bash のネットワーク通信先を許可ドメインに制限 |
| `sandbox.excludedCommands` | sandbox から除外するコマンド（git, docker は通常の permission で制御） |
| `sandbox.autoAllowBashIfSandboxed` | sandbox 内の Bash を自動承認（OS 制限内で安全に動かす） |
| `sandbox.allowUnsandboxedCommands` | sandbox 外での実行を禁止（false = 未対応コマンドはブロック） |
| `permissions.deny["Read(...)"]` | ファイル読み取り制限（sandbox ではなく permissions で制御） |

| 環境 | 実装 | 前提 |
|---|---|---|
| macOS | Seatbelt（OS 標準） | 追加インストール不要 |
| Linux/WSL2 | bubblewrap | `apt install bubblewrap socat` |
| WSL1 | 非サポート | - |

> **Sandbox enabled with auto-allow for bash commands** とは:
> サンドボックス内のため安全として Bash を自動承認する設定。
> このプロジェクトでは `autoAllowBashIfSandboxed: false` に設定し、ask ルールのプロンプトを維持している。

### 3層の多層防御

```
Layer 1: Permission Rules（Claude のポリシー制御）
  ├── allow: 日常的に使うコマンドで機密に触れないもの
  ├── ask: 必要だが影響が大きい操作（push, exec, gh）
  └── deny: 機密漏洩リスク・破壊的操作（最高優先度、sandbox 内でも必ず適用）

Layer 2: OS サンドボックス（seatbelt/bubblewrap）
  ├── ファイル書き込み: プロジェクトディレクトリ外は禁止（OS 強制）
  ├── 読み取り禁止: ~/.ssh, ~/.aws, ~/.config/gcloud（OS 強制）
  └── ネットワーク: github.com, pypi.org, docker.io のみ許可（OS 強制）

Layer 3: 運用ルール
  ├── 機密情報をチャットに貼らない
  └── 環境変数はマスクして共有
```

### ツール別 権限設計

| ツール | 用途 | 設定 |
|---|---|---|
| `Read` | ファイル読み取り | deny: `.env*`, `~/.ssh/*`, `~/.aws/*`, `*credentials*` など |
| `Edit` / `Write` | ファイル書き込み・編集 | deny: 同上（読めないものは書けない） |
| `Glob` / `Grep` | ファイル検索 | Read 権限に準拠 |
| `WebFetch` | 外部通信（API・ページ取得） | allow: 公式ドキュメント・GitHub のみ / ask: その他全て |
| `Bash` | コマンド実行 | allow: 日常コマンド / ask: push・exec・gh / deny: 危険操作 + Sandbox network |

### 禁止操作一覧

| カテゴリ | 禁止対象 | 適用ツール |
|---|---|---|
| 環境変数ファイル | `.env*`, `*.env` | Read / Edit / Write |
| Firebase | `google-services.json`, `GoogleService-Info.plist` | Read / Edit / Write |
| 署名鍵 | `*.keystore`, `*.jks`, `*.p12`, `*.pem` | Read / Edit / Write |
| クラウド認証（AWS） | `~/.aws/*` | Read / Edit / Write |
| クラウド認証（GCP） | `~/.config/gcloud/*`, `*service-account*.json` | Read / Edit / Write |
| SSH鍵 | `~/.ssh/*`, `*id_rsa*`, `*id_ed25519*` | Read / Edit / Write |
| 外部通信（Bash） | `curl`, `wget`, `nc`, `nmap`, `ssh`, `scp` | Bash deny + Sandbox network |
| 外部通信（WebFetch） | 未許可ドメインへのアクセス | WebFetch ask（許可外は確認） |
| 環境変数出力 | `printenv`, `env`, `export` | Bash |
| 破壊的操作 | `sudo`, `rm -rf`, `dd`, `mkfs`, `kill -9` | Bash |
| Git強制上書き | `git push --force`, `git push -f` | Bash |

### Claude Code 設定レベル

| レベル | ファイル | スコープ | Git |
|---|---|---|---|
| User | `~/.claude/settings.json` | 全プロジェクト共通 deny | 管理外 |
| Project | `.claude/settings.json` | このプロジェクト allow/ask/deny + sandbox | コミット済 |
| Local | `.claude/settings.local.json` | 個人上書き | gitignore |

<!-- MANUAL ADDITIONS END -->
