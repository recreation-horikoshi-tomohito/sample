from flask import Flask
from app.api.infrastructure.database import init_db
from app.api.presentation.employees import employees_bp


def create_app(database_url=None):
    app = Flask(__name__)

    if database_url:
        app.config["DATABASE"] = database_url

    init_db(app)
    app.register_blueprint(employees_bp)

    return app
