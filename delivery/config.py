"""Flask configuration."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    FLASK_APP = "delivery"
    TESTING = False
    DEBUG = False
    DB_NAME = None
    HOST = "0.0.0.0"
    PORT = 5000


class ProdConfig(Config):
    DB_NAME = environ.get("DB_NAME")
    HOST = "0.0.0.0"
    PORT = 5000


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    DB_NAME = 'mongodb://localhost/test'
    HOST = "127.0.0.1"
    PORT = 5000


