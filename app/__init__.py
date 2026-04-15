from flask import Flask
from flask_injector import FlaskInjector

from app.api.customers import bp as customers_bp
from app.module import AppModule


def create_app():
    app = Flask(__name__)

    app.register_blueprint(customers_bp)

    FlaskInjector(app=app, modules=[AppModule])

    return app
