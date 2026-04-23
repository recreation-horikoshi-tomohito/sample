import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    database_url = f"sqlite:///{db_path}"
    app = create_app(database_url=database_url)
    app.config["TESTING"] = True
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def db_session(app):
    engine = create_engine(app.config["DATABASE_URL"])
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def client(app):
    return app.test_client()
