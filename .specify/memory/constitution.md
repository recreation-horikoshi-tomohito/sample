<!--
SYNC IMPACT REPORT
==================
Version change: 1.1.0 → 1.3.0
原則変更:
  - I. オニオンアーキテクチャ → クリーンアーキテクチャ（層の再定義、ドメインサービス禁止追加）
  - V. エンティティ定義: @dataclass → __init__ に変更、entity/value_object ディレクトリ分離
セクション変更:
  - 開発環境 > ディレクトリ構成: domain/entity/, domain/value_object/ を追加
テンプレート更新状況:
  - ⚠ .specify/templates/plan-template.md（要手動確認: Constitution Check の原則 I 記述）
  - ✅ .specify/templates/spec-template.md（変更不要）
  - ✅ .specify/templates/tasks-template.md（変更不要）
保留中TODO: なし
-->

# 社員管理API Constitution

## 大前提

**このプロジェクトはテスト駆動開発（t_wadaのTDD）でプロジェクトを遂行することを大前提とする。**

t_wadaが提唱するTDDスタイルに従い、Red→Green→Refactorのサイクルを全ての機能実装において厳守する。
この大前提は全ての原則・判断に優先し、例外は認めない。

- 新機能の実装コードはテストが先に存在しなければならない（MUST）
- テストは実装前に書き、失敗（Red）を確認してから実装（Green）に移行する（MUST）
- テストなしの実装コードを追加してはならない（MUST NOT）
- `tests/presentation/` 配下にBlueprintに対応するテストファイルを配置する（MUST）

## Core Principles

### I. クリーンアーキテクチャ

依存方向は内側（Entities）に向かってのみ許可する（依存性逆転の原則）。
外側の層は内側を知ることができるが、内側は外側を知ってはならない。

- `domain/` 層は外部依存（Flask、SQLite等）を一切持ってはならない（MUST NOT）
- `infrastructure/` の変更は `domain/` と `usecase/` に影響してはならない（MUST NOT）
- ドメインサービスは使用しない（MUST NOT）
- **層を跨ぐ際は必ず定義済みの型（dataclass）に変換する（MUST）**
  - 入力側: `XxxInput` dataclass（例: `EmployeeInput`）
  - 出力側: `XxxOutput` dataclass（例: `EmployeeOutput`）
  - 型は `domain/<概念>/__init__.py` に定義する（MUST）
  - Entity 自体は変換メソッドを持たない。usecase 層で変換する（MUST）
- 各層の責務:
  - `domain/entity/`: エンティティ（IDを持つビジネスオブジェクト、最内層）
  - `domain/value_object/`: 値オブジェクト（IDを持たない、属性で同一性を判断）
  - `domain/repository/`: リポジトリインターフェース（抽象定義）
  - `usecase/`: ユースケース（アプリケーションビジネスルール）
  - `infrastructure/`: 外部依存（SQLite等）・具象実装
  - `presentation/`: FlaskのBlueprint（最外層・インターフェースアダプター）

**理由**: テスト容易性・変更への耐性・関心の分離。ビジネスロジックをフレームワーク
から独立させることで長期保守性を確保する。

### II. Blueprintパターン（1機能1ファイル）

FlaskのBlueprintを使い、1つの機能（リソース）に対して1つのファイルを割り当てる。

- presentation層の各Blueprintファイルは単一機能のみを担当する（MUST）
- Blueprintファイルに対応するテストファイルを `tests/presentation/` に置く（MUST）
- HTTPエラーレスポンスは400（クライアントエラー）または500（サーバーエラー）のみ（MUST）
- APIレスポンスはJSON形式で返す（MUST）

**理由**: 機能の局所化により変更影響範囲を最小化し、テストとの対応関係を明確にする。

### III. シンプリシティ（徹底的なシンプルさ）

例外処理・入力バリデーション・コードは極限までシンプルに保つ。

- 型アノテーションは記述しない（SHOULD NOT）
- ロギング実装は追加しない（MUST NOT）
- 例外・入力処理は最小限に留める（MUST）
- YAGNIを徹底する: 現在必要でない機能・抽象化を追加してはならない（MUST NOT）
- DBはSQLiteのみを使用する（MUST）

**理由**: シンプルなコードは読みやすく、保守しやすく、バグが少ない。
この規模のアプリに不要な複雑さを持ち込まない。

### IV. 日本語ドキュメント

全てのドキュメント・コメント・コミットメッセージ・AIへの回答は日本語で記述する。

- スペック・計画・タスク等のSpecKitドキュメントはすべて日本語で書く（MUST）
- コード内コメントが必要な場合は日本語で書く（MUST）
- AIエージェントへの回答・提案は日本語で行う（MUST）

**理由**: チームの共通言語が日本語であり、ドキュメントの可読性と保守性を最大化する。

### V. インターフェース分離と依存性注入

`core`（domain + usecase）と `infrastructure` をインターフェースで明確に分離し、
`injector` ライブラリによる DI でバインディングを一元管理する。

**インターフェース（core側）**:

- ドメイン概念ごとにサブディレクトリを切る（例: `domain/employee/`）（MUST）
- 値オブジェクト / DTO は `domain/<概念>/__init__.py` に `@dataclass` で定義する（MUST）
- エンティティは `domain/<概念>/<概念>.py` に通常クラスで定義し、フィールドは `__init__` に書く（MUST）
- リポジトリインターフェースは `domain/repository/` に別ファイルで配置する（MUST）
- `abc.ABC` + `@abstractmethod` でインターフェースを定義する（MUST）
- 命名規則: `I` プレフィックス（例: `IEmployeeRepository`）（MUST）

```python
# app/api/domain/employee/__init__.py  ← 値オブジェクト / DTO
from dataclasses import dataclass

@dataclass
class EmployeeData:
    name: str
    role: str
    ...

# app/api/domain/employee/employee.py  ← エンティティ（ロジック）
class Employee:
    def __init__(self, id: int, name: str, ...):
        self.id = id
        ...

# app/api/domain/repository/employee_repository.py  ← インターフェース
from abc import ABC, abstractmethod
from app.api.domain.employee.employee import Employee

class IEmployeeRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Employee]:
        raise NotImplementedError
```

**ユースケース（core/usecase/ 側）**:

- ユースケースは **シングルアクション** とする。1クラス1メソッド（`execute`）のみを持つ（MUST）
- 1つのユースケースクラスが担う責務は1つのユーザー操作に限定する（MUST）
- ユースケースごとにファイルを分割する（例: `find_employee_list.py`）（MUST）
- インターフェースは `usecase/<概念>/__init__.py` に定義し、具象クラスは別ファイルに実装する（MUST）
- 命名規則: インターフェースは `IXxxUseCase`、具象クラスは `XxxUseCase`（MUST）

**具象実装（infrastructure側）**:

- 具象クラスは `infrastructure/repository/` に配置する（MUST）
- 具象クラスはインターフェースを継承して実装する（MUST）
- `usecase/` 層が `infrastructure/` モジュールを直接 import してはならない（MUST NOT）

**DI設定（module.py）**:

- `injector.Module` を継承した `AppModule` を `app/module.py` に配置する（MUST）
- `binder.bind(IXxx, to=ConcreteXxx)` でバインディングを宣言する（MUST）
- Flask アプリへの注入は `injector` のみを使い、`app.injector = Injector([AppModule()])` で設定する（MUST）

```python
# app/module.py
from injector import Module
from app.api.domain.repository.employee_repository import IEmployeeRepository
from app.api.infrastructure.repository.employee_repository import SQLiteEmployeeRepository

class AppModule(Module):
    def configure(self, binder):
        binder.bind(IEmployeeRepository, to=SQLiteEmployeeRepository)
```

**理由**: infrastructure（SQLite等）を差し替え可能にし、usecase のテストで
モック/スタブに置き換えやすくする。テスト容易性と変更耐性を高める。

## 技術スタック

- **言語**: Python 3.12
- **フレームワーク**: Flask 3.1
- **パッケージ管理**: uv
- **静的解析・フォーマット**: ruff
- **ビルドツール**: hatchling
- **テストフレームワーク**: pytest 8.3.5
- **データベース**: SQLite
- **コンテナ**: Docker（`docker compose up -d` で起動、ホスト8081→コンテナ5000）

## 開発環境

**ディレクトリ構成**:

```
app/
├── __init__.py
└── api/
    ├── core/                # ビジネスロジック（最内層）
    │   ├── domain/
    │   │   ├── <概念>/      # ドメイン概念ごとのディレクトリ（例: employee/）
    │   │   │   ├── __init__.py  # @dataclass 値オブジェクト / DTO
    │   │   │   └── <概念>.py    # エンティティ（__init__でフィールド定義＋ロジック）
    │   │   └── repository/  # リポジトリインターフェース（IXxxRepository(ABC)）
    │   └── usecase/         # アプリケーションビジネスルール
    │       # ※ admin / user 等の機能別サブディレクトリ分割は未決定
    ├── infrastructure/      # 外部依存
    │   ├── models/          # SQLAlchemy ORM モデル
    │   └── repository/      # 具象実装（IXxxRepository を継承）
    └── presentation/        # FlaskのBlueprint（最外層）
app/module.py                # AppModule: injector によるバインディング定義
tests/
├── core/
│   └── usecase/             # usecase層インテグレーションテスト
├── infrastructure/
│   └── repository/          # リポジトリ層インテグレーションテスト
└── presentation/            # Blueprintファイルに対応するテストファイル
```

**起動方法**:

```bash
docker compose up -d
```

**アクセス先**: `http://localhost:8081`（内部: `0.0.0.0:5000`）

## Governance

本Constitutionはプロジェクトの全実装判断に優先する。
修正には以下のプロセスが必要：

- **修正手順**: 変更内容をユーザーに説明し、バージョンをインクリメントし、影響するテンプレートを同期する
- **バージョンポリシー**:
  - MAJOR: 大前提・原則の廃止または根本的再定義（後方非互換）
  - MINOR: 新原則・新セクションの追加または大幅な拡張
  - PATCH: 文言修正・明確化・タイポ修正など非意味的な変更
- **コンプライアンスレビュー**: 各PR・タスク実装時にConstitution Checkを実施する
- **ガイダンス**: ランタイム開発ガイダンスは `.specify/memory/` 配下のドキュメントを参照

**Version**: 1.3.0 | **Ratified**: 2026-04-20 | **Last Amended**: 2026-04-23
