"""
This module create all env variables for application
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Config for loading constants from env or default values
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_HOST = os.environ.get('FLASK_HOST') or '127.0.0.1'
    FLASK_PORT = os.environ.get('FLASK_RUN_PORT') or '6000'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

