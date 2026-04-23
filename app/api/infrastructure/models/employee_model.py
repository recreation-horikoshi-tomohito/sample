from sqlalchemy import Column, Integer, String, CheckConstraint
from app.api.infrastructure.models import Base


class EmployeeModel(Base):
    """
    社員テーブルの SQLAlchemy ORM モデル。infrastructure 層に属し、
    employees テーブルと対応する。Base.metadata.create_all() でスキーマを自動生成する。
    status カラムには CHECK 制約（在籍中 / 退職済）を設定する。
    """
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
