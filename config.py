"""
This module create all env variables for application
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Config for loading constants from env or default values
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_HOST = os.environ.get('FLASK_HOST')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_HOST = os.environ.get('FLASK_HOST') or '127.0.0.1'
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT') or '6000'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')