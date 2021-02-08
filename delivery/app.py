import json
import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from delivery.error_handling import CustomError
from flasgger import Swagger
from marshmallow import ValidationError
from delivery.routes import RestaurantEndpoint, RestaurantItemEndpoint
from delivery.repositories import MemoryRestaurantRepository, MongoRepository, AbstractRestaurantRepository
from delivery.schemas import RestaurantCreateOrUpdateSchema
from pymongo import MongoClient


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


def register_error_handlers(app: Flask):
    app.register_error_handler(CustomError, handle_standard_exception)
    app.register_error_handler(HTTPException, handle_standard_exception)
    app.register_error_handler(ValidationError, handle_validation_error)


# def read_restaurants(path: str, repository: MemoryRestaurantRepository) -> None:
#     try:
#         with open(path, "r") as read_file:
#             data = json.load(read_file)
#             schema = RestaurantCreateOrUpdateSchema()
#             for restaurant in data['restaurants']:
#                 a = schema.load(restaurant)
#                 repository.create(a)
#     except TypeError:
#         raise TypeError("Set environment variable: PATH_FOR_INITIAL_DATA")


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
    #path = application.config.get('PATH_FOR_INITIAL_DATA', 'restaurants.json')
    application.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    #mongo = PyMongo(application)
    client = MongoClient('localhost', 27017)
    db = client.test
    repository = MongoRepository(db)
    # repository = MemoryRestaurantRepository()
    # read_restaurants(path, repository)
    register_url_rules(application, repository)
    register_error_handlers(application)

    return application


app = create_app()


if __name__ == '__main__':
    app.run(app.config.get("HOST"), port=int(app.config.get("PORT", 5000)))

