# 実装計画: 社員一覧

**Branch**: `feature/001-employee-list` | **Date**: 2026-04-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-employee-list/spec.md`

## Summary

在籍中の社員の情報（氏名・役職・部署・年齢・勤続年数）をJSON形式で返すREST APIエンドポイントを実装する。
オニオンアーキテクチャに従い、domain → usecase → infrastructure → presentation の順に設計し、
TDD大前提のもと、presentationテストを先に書いてからBlueprint実装に進む。

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: Flask 3.1、uv（パッケージ管理）、ruff（静的解析・フォーマット）
**Storage**: SQLite
**Testing**: pytest 8.3.5
**Target Platform**: Dockerコンテナ（Linux、ホスト8081→コンテナ5000）
**Project Type**: RESTful Web API（バックエンドのみ）
**Performance Goals**: 社員一覧取得が1秒以内に完了（SC-001）
**Constraints**: ロギング不要・型アノテーション不要・例外処理は最小限・YAGNIを徹底
**Scale/Scope**: 小〜中規模の社員管理アプリ（全件取得のみ、ページネーションなし）

## Constitution Check

*GATE: Phase 0 リサーチ前に通過必須。Phase 1 設計後に再確認。*

| 原則 | ゲート条件 | 状態 |
|------|-----------|------|
| 大前提: TDD | `tests/presentation/test_employees.py` を先に作成し、失敗を確認してから実装へ | ✅ 計画に反映済み |
| I. オニオンアーキテクチャ | `domain/employee.py` → `usecase/get_employees.py` → `infrastructure/employee_repository.py` → `presentation/employees.py` の一方向依存 | ✅ 計画に反映済み |
| II. Blueprintパターン | `presentation/employees.py` という1ファイルで社員一覧機能を担当 | ✅ 計画に反映済み |
| III. シンプリシティ | ロギングなし・型アノテーションなし・例外処理は最小限 | ✅ 計画に反映済み |
| IV. 日本語ドキュメント | 全ドキュメントを日本語で記述 | ✅ 対応済み |

**Phase 1 設計後の再確認**: ✅ データモデル・コントラクトともにアーキテクチャ違反なし

## Project Structure

### Documentation（本機能）

```text
specs/001-employee-list/
├── plan.md              # 本ファイル（/speckit-plan コマンド出力）
├── spec.md              # 機能仕様
├── research.md          # Phase 0 出力
├── data-model.md        # Phase 1 出力
├── quickstart.md        # Phase 1 出力
├── contracts/           # Phase 1 出力
│   └── get-employees.md
└── checklists/
    └── requirements.md
```

### Source Code（リポジトリルート）

```text
app/
└── api/
    ├── domain/
    │   └── employee.py              # Employeeエンティティ（最内層）
    ├── usecase/
    │   └── get_employees.py         # 社員一覧取得ユースケース
    ├── infrastructure/
    │   └── employee_repository.py   # SQLiteリポジトリ
    └── presentation/
        └── employees.py             # Flask Blueprint（最外層）

tests/
└── presentation/
    └── test_employees.py            # Blueprintのテスト（TDD: 先に作成）
```

**Structure Decision**: オニオンアーキテクチャに従いシングルプロジェクト構成。
依存方向は `presentation → usecase → domain` の一方向のみ。

## Complexity Tracking

> Constitution Checkに違反なし。記録事項なし。
