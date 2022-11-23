from flask import Flask
from config import Config


def create_app(config_class=Config):
    """
    Create app and loading config
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app
