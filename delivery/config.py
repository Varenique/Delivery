"""Flask configuration."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    FLASK_APP = "delivery"
    TESTING = False
    DEBUG = False
    DB_CONNECTION = None
    PATH_FOR_INITIAL_DATA = None
    HOST = "0.0.0.0"
    PORT = 5000


class ProdConfig(Config):
    PATH_FOR_INITIAL_DATA = environ.get("PATH_FOR_INITIAL_DATA")
    DB_CONNECTION = environ.get("DB_CONNECTION")
    HOST = "0.0.0.0"
    PORT = 5000


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    PATH_FOR_INITIAL_DATA = path.join(basedir, 'restaurants.json')
    DB_CONNECTION = 'mongodb://localhost:27017/'
    HOST = "127.0.0.1"
    PORT = 5000


