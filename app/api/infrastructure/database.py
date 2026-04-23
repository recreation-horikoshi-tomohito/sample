from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g


def get_session(app):
    if "db_session" not in g:
        engine = create_engine(app.config.get("DATABASE_URL", "sqlite:///employees.db"))
        Session = sessionmaker(bind=engine)
        g.db_session = Session()
    return g.db_session


def init_db(app):
    from app.api.infrastructure.models import Base
    engine = create_engine(app.config.get("DATABASE_URL", "sqlite:///employees.db"))
    Base.metadata.create_all(engine)

    @app.teardown_appcontext
    def close_session(e=None):
        session = g.pop("db_session", None)
        if session is not None:
            session.close()
