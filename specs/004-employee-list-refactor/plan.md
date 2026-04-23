# Implementation Plan: 社員一覧リファクタリング

**Branch**: `feature/issues-15` | **Date**: 2026-04-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/004-employee-list-refactor/spec.md`

## Summary

社員一覧・社員詳細の内部構造を Constitution v1.1.0 原則 V に準拠させる。
`domain/repository/` にインターフェース（`abc.ABC`）と `@dataclass` エンティティを定義し、
`infrastructure/repository/` に具象実装を置き、`flask-injector` + `module.py` で DI を一元管理する。
外部 API 仕様（レスポンス・ステータスコード）は一切変更しない。

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: Flask 3.1、flask-injector（新規追加）、injector（flask-injector の依存）、pytest 8.3.5
**Storage**: SQLite（既存スキーマ変更不要）
**Testing**: pytest 8.3.5（既存テストをそのまま使用）
**Target Platform**: Docker コンテナ（Linux）
**Project Type**: REST API（Web サービス）リファクタリング
**Performance Goals**: 既存動作を維持（特別な目標なし）
**Constraints**: シンプリシティ原則維持・外部 API 仕様不変・既存テストを全て通過
**Scale/Scope**: 社員一覧・社員詳細エンドポイントのみ（2 ユースケース）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 原則 | チェック | 判定 |
|---|---|---|
| TDD（大前提） | 既存テスト（Green）がある → Refactor フェーズとして実施。US2 の新テストは Red→Green で追加 | ✅ |
| オニオンアーキテクチャ | `domain/repository/` にIF定義、usecase は interface 経由のみ、infrastructure は最外層 | ✅ |
| Blueprint パターン | `employees.py` の 1 ファイル・2 エンドポイント構成を維持 | ✅ |
| シンプリシティ | YAGNI 例外（原則 V）＋`@dataclass` の型アノテーション（SHOULD NOT だが原則 V で必須） | ⚠️ * |
| 日本語ドキュメント | 全ドキュメント日本語 | ✅ |
| インターフェース分離と DI（原則 V） | これが本リファクタリングの目的 | ✅ |

\* **Complexity Tracking**:

| 違反 | 必要な理由 | よりシンプルな代替を取らない理由 |
|---|---|---|
| `@dataclass` の型アノテーション（SHOULD NOT） | `@dataclass` 自体が原則 V の MUST 要件であり、型なしでは動作しない | plain class では原則 V を満たせない |
| flask-injector の追加 | 原則 V「flask-injector を使用する（MUST）」 | 手動 DI でも可能だが原則 V が flask-injector を明示 |

## Project Structure

### Documentation (this feature)

```text
specs/004-employee-list-refactor/
├── plan.md              # このファイル
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # /speckit-tasks で生成
```

### Source Code（変更・追加・削除対象）

```text
app/
├── __init__.py                              # 変更: FlaskInjector(app, [AppModule()]) を追加
├── module.py                                # 新規: AppModule（DI バインディング）
└── api/
    ├── domain/
    │   ├── employee.py                      # 削除: エンティティを domain/repository/ へ移動
    │   └── repository/                      # 新規ディレクトリ
    │       ├── __init__.py                  # 新規
    │       └── employee_repository.py       # 新規: @dataclass Employee + IEmployeeRepository(ABC)
    ├── usecase/
    │   ├── get_employees.py                 # 変更: 関数 → GetEmployeesUseCase クラス
    │   └── get_employee.py                  # 変更: 関数 → GetEmployeeUseCase クラス
    ├── infrastructure/
    │   ├── employee_repository.py           # 削除: 具象実装を infrastructure/repository/ へ移動
    │   └── repository/                      # 新規ディレクトリ
    │       ├── __init__.py                  # 新規
    │       └── employee_repository.py       # 新規: SQLiteEmployeeRepository(IEmployeeRepository)
    └── presentation/
        └── employees.py                     # 変更: @inject デコレータを追加

requirements.txt                             # 変更: flask-injector を追加
```

**スコープ補足**: spec は「社員一覧のみ」だが、`IEmployeeRepository` は `find_all`・`find_by_id` の両メソッドを定義する。社員詳細ユースケースも同一インターフェースを使うため、半移行状態を避けて同時にリファクタリングする。

### 実装方針

**エンティティ + インターフェース（domain/repository/employee_repository.py）**:

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import date

@dataclass
class Employee:
    id: int
    name: str
    role: str
    position: str
    department: str
    age: int
    hire_date: str

    @property
    def years_of_service(self):
        hired = date.fromisoformat(self.hire_date)
        today = date.today()
        return (today.year - hired.year) - (
            1 if (today.month, today.day) < (hired.month, hired.day) else 0
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "position": self.position,
            "department": self.department,
            "age": self.age,
            "hire_date": self.hire_date,
            "years_of_service": self.years_of_service,
        }

class IEmployeeRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Employee]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, employee_id: int) -> Employee | None:
        raise NotImplementedError
```

**具象実装（infrastructure/repository/employee_repository.py）**:

- `IEmployeeRepository` を継承
- `current_app._get_current_object()` 経由で `get_db()` を呼ぶ（infrastructure は Flask 依存 OK）

**usecase（クラスに変更）**:

```python
# get_employees.py
from app.api.domain.repository.employee_repository import IEmployeeRepository

class GetEmployeesUseCase:
    def __init__(self, repo: IEmployeeRepository):
        self.repo = repo

    def execute(self):
        return [e.to_dict() for e in self.repo.find_all()]
```

**presentation（@inject 追加）**:

```python
from flask_injector import inject

@employees_bp.route("/api/employees")
@inject
def list_employees(usecase: GetEmployeesUseCase):
    return jsonify(usecase.execute())
```

**module.py（DI バインディング）**:

```python
from injector import Module
from app.api.domain.repository.employee_repository import IEmployeeRepository
from app.api.infrastructure.repository.employee_repository import SQLiteEmployeeRepository

class AppModule(Module):
    def configure(self, binder):
        binder.bind(IEmployeeRepository, to=SQLiteEmployeeRepository)
```

**create_app() 変更**:

```python
from flask_injector import FlaskInjector
from app.module import AppModule

def create_app(database_url=None):
    app = Flask(__name__)
    if database_url:
        app.config["DATABASE"] = database_url
    init_db(app)
    app.register_blueprint(employees_bp)
    FlaskInjector(app=app, modules=[AppModule()])
    return app
```

**既存テストへの影響**:
- `conftest.py` は `create_app()` を呼ぶだけなので変更不要
- `seed()` 関数は `get_db(app)` を直接呼ぶため変更不要
- 全テストがリファクタリング後もそのままパスする
