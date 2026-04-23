# Data Model: リポジトリ層・ユースケース層テスト + SQLAlchemy移行

## エンティティ: Employee（ドメイン層）

`app/api/domain/employee/employee.py`

| フィールド | 型 | 説明 |
|-----------|-----|------|
| id | int | 社員ID（主キー） |
| name | str | 氏名 |
| role | str | 役割（エンジニア等） |
| position | str | 職位（主任・一般等） |
| department | str | 部署名 |
| age | int | 年齢 |
| hire_date | str | 入社日（ISO形式: YYYY-MM-DD） |

**ビジネスロジック**:
- `years_of_service`: hire_dateから現在日付までの勤続年数（端数切り捨て）

**注意**: `status` はドメインエンティティには含まない。リポジトリがDBから `在籍中` のみをフィルタしてエンティティを返す責務を持つ。

---

## ORMモデル: EmployeeModel（infrastructure層）

`app/api/infrastructure/models/employee_model.py`

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | Integer | PRIMARY KEY, AUTOINCREMENT | 社員ID |
| name | String | NOT NULL | 氏名 |
| role | String | NOT NULL | 役割 |
| position | String | NOT NULL | 職位 |
| department | String | NOT NULL | 部署名 |
| age | Integer | NOT NULL | 年齢 |
| hire_date | String | NOT NULL | 入社日（YYYY-MM-DD） |
| status | String | NOT NULL, DEFAULT='在籍中' | 在籍状態 |

**テーブル名**: `employees`

**ステータス制約**: `status` は `在籍中` または `退職済` のみ許可（CheckConstraint）

**ORMクラス定義**:
```python
# app/api/infrastructure/models/__init__.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# app/api/infrastructure/models/employee_model.py
from sqlalchemy import Column, Integer, String, CheckConstraint
from app.api.infrastructure.models import Base

class EmployeeModel(Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint("status IN ('在籍中', '退職済')", name="status_check"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    position = Column(String, nullable=False)
    department = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    hire_date = Column(String, nullable=False)
    status = Column(String, nullable=False, default="在籍中")
```

---

## DTO: EmployeeOutput（usecase→presentation境界）

`app/api/domain/employee/__init__.py`

| フィールド | 型 | 説明 |
|-----------|-----|------|
| id | int | 社員ID |
| name | str | 氏名 |
| role | str | 役割 |
| position | str | 職位 |
| department | str | 部署名 |
| age | int | 年齢 |
| hire_date | str | 入社日 |
| years_of_service | int | 勤続年数（計算済み） |

**注意**: `status` は含まない（presentation層に公開しない）

---

## レイヤー間のデータフロー

```
SQLite DB
  ↓ EmployeeModel（ORM）
SQLiteEmployeeRepository
  ↓ Employee（エンティティ）
FindEmployeeListUseCase / FindEmployeeDetailUseCase
  ↓ EmployeeOutput（DTO）
presentation層 / テスト
```

---

## 関係

- `EmployeeModel` (infrastructure) → `Employee` (domain): リポジトリが変換
- `Employee` (domain) → `EmployeeOutput` (domain/DTO): usecase層が変換
- `Base` (infrastructure/models): `EmployeeModel` の親クラス（スキーマ自動生成の起点）
