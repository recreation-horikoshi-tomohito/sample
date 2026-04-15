from flask import Flask
from flask_injector import FlaskInjector
from app.module import AppModule


def create_app():
    app = Flask(__name__)

    FlaskInjector(app=app, modules=[AppModule])

    return app
