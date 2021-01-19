import os

from flasgger import Swagger
from flask import Flask


def create_app():
    application = Flask(__name__)
    application.config.from_object('config.Config')
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        application.config.from_object('config.DevConfig')
    else:
        os.environ['FLASK_ENV'] = 'production'
        application.config.from_object('config.ProdConfig')

    Swagger(application)
    from . import app
    application.register_blueprint(app.bp)
    return application
