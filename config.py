"""Flask configuration."""
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    TESTING = False
    DEBUG = False
    PATH_FOR_INITIAL_DATA = None


class ProdConfig(Config):
    PATH_FOR_INITIAL_DATA = os.environ.get("PATH_FOR_INITIAL_DATA")


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    PATH_FOR_INITIAL_DATA = path.join(basedir, 'restaurants.json')
