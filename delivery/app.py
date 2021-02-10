import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from delivery.error_handling import CustomError
from flasgger import Swagger
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from pymongo import MongoClient
from delivery.routes import RestaurantEndpoint, RestaurantItemEndpoint, LoginEndpoint
from delivery.repositories import MongoRestaurantRepository, AbstractRestaurantRepository
from delivery.schemas import RestaurantCreateOrUpdateSchema


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


def register_url_rules(app: Flask, restaurants: AbstractRestaurantRepository):
    app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api",
                                                                              restaurants,
                                                                              RestaurantCreateOrUpdateSchema()))
    app.add_url_rule("/api/restaurants/<restaurant_id>",
                     view_func=RestaurantItemEndpoint.as_view("restaurant_item_api",
                                                              restaurants,
                                                              RestaurantCreateOrUpdateSchema(partial=True)))

    app.add_url_rule("/api/login", view_func=LoginEndpoint.as_view("login_api",
                                                                   restaurants, RestaurantCreateOrUpdateSchema()))


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
    application.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    jwt = JWTManager(application)
    mongo_client = MongoClient(application.config['DB_CONNECTION'])
    db = mongo_client.delivery
    repository = MongoRestaurantRepository(db)

    register_url_rules(application, repository)
    register_error_handlers(application)

    return application


app = create_app()


if __name__ == '__main__':
    app.run(app.config.get("HOST"), port=int(app.config.get("PORT", 5000)))

