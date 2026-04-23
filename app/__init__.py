from flask import Flask
from injector import Injector
from app.api.infrastructure.database import init_db
from app.api.presentation.employees import employees_bp
from app.module import AppModule


def create_app(database_url=None):
    app = Flask(__name__)

    app.config["DATABASE_URL"] = database_url or "sqlite:///employees.db"

    init_db(app)
    app.register_blueprint(employees_bp)
    app.injector = Injector([AppModule()])

    return app
