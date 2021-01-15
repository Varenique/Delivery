from flask import Flask


def create_app():
    application = Flask(__name__)
    application.config.from_object('config.Config')

    from . import app
    application.register_blueprint(app.bp)
    return application
