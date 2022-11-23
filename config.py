"""
This module create all env variables for application
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Class for configure applictaion
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_HOST = os.environ.get('FLASK_HOST')
    FLASK_PORT = os.environ.get('FLASK_PORT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

