from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import ProductionConfig, DevelopmentConfig, TestingConfig

db = SQLAlchemy()
migrate = Migrate()

profilies = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'testing': TestingConfig()
}

def create_app(profile):
    """
    Create app and loading config
    """
    app = Flask(__name__)
    app.config.from_object(profilies[profile])
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models
