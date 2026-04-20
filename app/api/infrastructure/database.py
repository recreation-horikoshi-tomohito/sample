import sqlite3
import os
from flask import g

_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db(app):
    if "db" not in g:
        g.db = sqlite3.connect(app.config.get("DATABASE", "employees.db"))
        g.db.row_factory = sqlite3.Row
        with open(_SCHEMA) as f:
            g.db.executescript(f.read())
    return g.db


def init_db(app):
    @app.teardown_appcontext
    def close_db(e=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()
