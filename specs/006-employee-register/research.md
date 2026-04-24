# Research: 社員登録機能

**Feature**: 社員登録機能（#22）
**Date**: 2026-04-24

## 調査項目なし

本機能は既存スタック・アーキテクチャと完全に整合しており、NEEDS CLARIFICATIONは存在しない。
以下に確定済みの設計判断を記録する。

---

## Decision 1: 登録レスポンスDTO

- **Decision**: `EmployeeCreateOutput`（新規 dataclass）を使用する
- **Rationale**: 既存の `EmployeeOutput` は `years_of_service` を含み `status` を持たない。登録直後のレスポンスは `status="在籍中"` の確認が必要だが `years_of_service` は不要（YAGNI）。
- **Alternatives considered**: `EmployeeOutput` 再利用 → status が含まれないため不適切

## Decision 2: リポジトリインターフェースへの `save` 追加

- **Decision**: `IEmployeeRepository` に `save(input: EmployeeInput) -> Employee` を追加する
- **Rationale**: 既存の `find_all` / `find_by_id` と同一インターフェースに登録操作を集約することで、モジュール境界を維持する（Constitution V準拠）
- **Alternatives considered**: 別リポジトリインターフェースを作成 → YAGNI違反（同一エンティティの操作は1インターフェースに統合が自然）

## Decision 3: バリデーション戦略

- **Decision**: presentation層で `request.get_json()` の結果を検査し、必須フィールド欠落・型不正を400で返す。それ以外（DB障害等）は500とする
- **Rationale**: Constitution III「例外・入力処理は最小限（MUST）」に従い、専用バリデーターライブラリは使わず最小限のチェックのみ実施
- **Alternatives considered**: marshmallow / pydantic → 依存追加・YAGNI違反

## Decision 4: ルートパス

- **Decision**: `POST /api/employees`
- **Rationale**: 既存の `GET /api/employees` と同一Blueprint・同一パスで HTTP メソッドのみ分岐（Flask routing）
- **Alternatives considered**: `/api/employees/create` → RESTful でない
