import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from delivery.error_handling import CustomError
from flasgger import Swagger
from marshmallow import ValidationError
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from delivery.routes import RestaurantEndpoint, RestaurantItemEndpoint, LoginEndpoint, RegisterEndpoint
from delivery.repositories import MongoRestaurantRepository, AbstractRestaurantRepository, AbstractUserRepository, MongoUserRepository
from delivery.schemas import RestaurantCreateOrUpdateSchema, UserSchema


def handle_validation_error(ex):
    return jsonify({
        "name": "Bad Request",
        "description": ex.messages
    }), 400


def handle_standard_exception(ex):
    return jsonify({
        "name": ex.name,
        "description": ex.description,
    }), ex.code


def register_url_rules(app: Flask, repository: AbstractRestaurantRepository, user_repository: AbstractUserRepository):
    app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api",
                                                                              repository,
                                                                              RestaurantCreateOrUpdateSchema()))
    app.add_url_rule("/api/restaurants/<restaurant_id>",
                     view_func=RestaurantItemEndpoint.as_view("restaurant_item_api",
                                                              repository,
                                                              RestaurantCreateOrUpdateSchema(partial=True)))

    app.add_url_rule("/api/login", view_func=LoginEndpoint.as_view("login_api",
                                                                   user_repository,
                                                                   UserSchema()))
    app.add_url_rule("/api/register", view_func=RegisterEndpoint.as_view("register_api",
                                                                         user_repository,
                                                                         UserSchema()))


def register_error_handlers(app: Flask):
    app.register_error_handler(CustomError, handle_standard_exception)
    app.register_error_handler(HTTPException, handle_standard_exception)
    app.register_error_handler(ValidationError, handle_validation_error)


def create_app() -> Flask:
    application = Flask(__name__)
    application.config.from_object('delivery.config.Config')
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        application.config.from_object('delivery.config.DevConfig')
    else:
        os.environ['FLASK_ENV'] = 'production'
        application.config.from_object('delivery.config.ProdConfig')
    application.config['SWAGGER'] = {
        "uiversion": 3,
        "openapi": "3.0.3",
        'title': 'Delivery System API',
        'description': 'Documentation for Delivery App by Varvara M.',
        'doc_dir': './apidocs/'
    }
    Swagger(application)

    jwt = JWTManager(application)
    mongo_client = MongoClient(application.config['DB_CONNECTION'])
    db = mongo_client.delivery
    repository = MongoRestaurantRepository(db)

    register_url_rules(application, repository, MongoUserRepository(db))
    register_error_handlers(application)

    return application


app = create_app()


if __name__ == '__main__':
    app.run(app.config.get("HOST"), port=int(app.config.get("PORT", 5000)))

