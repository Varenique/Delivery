"""Flask configuration."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    TESTING = False
    DEBUG = False
    PATH_FOR_INITIAL_DATA = None


class ProdConfig(Config):
    PATH_FOR_INITIAL_DATA = environ.get("PATH_FOR_INITIAL_DATA")


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    PATH_FOR_INITIAL_DATA = path.join(basedir, 'restaurants.json')

