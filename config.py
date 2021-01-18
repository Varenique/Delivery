"""Flask configuration."""
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    TESTING = False
    DEBUG = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    PATH_FOR_INITIAL_DATA = os.environ.get("PATH_FOR_INITIAL_DATA") or path.join(basedir, 'restaurants.json')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    PATH_FOR_INITIAL_DATA = path.join(basedir, 'restaurants.json')
