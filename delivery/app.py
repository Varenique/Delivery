import json
import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from delivery.error_handling import CustomError
from flasgger import Swagger
from marshmallow import ValidationError
from delivery.models import RestaurantEndpoint, RestaurantItemEndpoint
from delivery.repositories import MemoryRestaurantRepository
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


def register_url_rules(app, restaurants):
    app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api", restaurants))
    app.add_url_rule("/api/restaurants/<int:restaurant_id>",
                     view_func=RestaurantItemEndpoint.as_view("restaurant_item_api", restaurants))


def register_error_handlers(app):
    app.register_error_handler(CustomError, handle_standard_exception)
    app.register_error_handler(HTTPException, handle_standard_exception)
    app.register_error_handler(ValidationError, handle_validation_error)


def read_restaurants(path, repository):
    try:
        with open(path, "r") as read_file:
            data = json.load(read_file)
            schema = RestaurantCreateOrUpdateSchema()
            for restaurant in data['restaurants']:
                a = schema.load(restaurant)
                repository.create(a)
    except TypeError:
        raise TypeError("Set environment variable: PATH_FOR_INITIAL_DATA")


def create_app():
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
    path = application.config.get('PATH_FOR_INITIAL_DATA', 'restaurants.json')
    repository = MemoryRestaurantRepository()
    read_restaurants(path, repository)
    register_url_rules(application, repository)
    register_error_handlers(application)
    return application


app = create_app()


if __name__ == '__main__':
    app.run(app.config.get("HOST"), port=int(app.config.get("PORT", 5000)))

