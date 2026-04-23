from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy ORM の基底クラス。
    全 ORM モデルはこの Base を継承し、Base.metadata.create_all() でスキーマを自動生成する。
    """
    pass
