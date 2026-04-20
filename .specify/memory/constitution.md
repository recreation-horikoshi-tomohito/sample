<!--
SYNC IMPACT REPORT
==================
Version change: (template) → 1.0.0
原則追加:
  - [前提] テスト駆動開発（t_wadaのTDD）によるプロジェクト遂行
  - I. オニオンアーキテクチャ
  - II. Blueprintパターン（1機能1ファイル）
  - III. シンプリシティ（徹底的なシンプルさ）
  - IV. 日本語ドキュメント
セクション追加:
  - 大前提（TDD）
  - 技術スタック
  - 開発環境
セクション削除: なし（テンプレートプレースホルダーを置換）
テンプレート更新状況:
  - ✅ .specify/templates/plan-template.md（Constitution Checkセクション確認済み・変更不要）
  - ✅ .specify/templates/spec-template.md（確認済み・変更不要）
  - ✅ .specify/templates/tasks-template.md（TDDタスク順序が大前提と整合済み）
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

### I. オニオンアーキテクチャ

依存方向は内側（domain）に向かってのみ許可する。
`presentation → usecase → domain` の一方向依存を厳守する。

- `domain/` 層は外部依存（Flask、SQLite等）を一切持ってはならない（MUST NOT）
- `infrastructure/` の変更は `domain/` と `usecase/` に影響してはならない（MUST NOT）
- 各層の責務:
  - `domain/`: エンティティ・ビジネスロジック（最内層）
  - `usecase/`: ユースケース
  - `infrastructure/`: 外部依存（SQLite等）
  - `presentation/`: FlaskのBlueprint（最外層）

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
    ├── domain/          # エンティティ・ビジネスロジック（最内層）
    ├── usecase/         # ユースケース
    ├── infrastructure/  # 外部依存（SQLite等）
    └── presentation/    # FlaskのBlueprint（最外層）
tests/
└── presentation/        # Blueprintファイルに対応するテストファイル
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

**Version**: 1.0.0 | **Ratified**: 2026-04-20 | **Last Amended**: 2026-04-20
