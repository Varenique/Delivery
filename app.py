import json
import os
from flask import Flask, request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import HTTPException
from error_handling import CustomError, WrongIdError
from flasgger import Swagger, SwaggerView, Schema, fields
from marshmallow import Schema, fields, ValidationError


class RestaurantCreateOrUpdateSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    work_time = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    id = fields.Int(dump_only=True)


class RestaurantEndpoint(MethodView):
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def get(self):
        return jsonify(self.restaurants), 200

    def post(self):
        content = request.json
        schema = RestaurantCreateOrUpdateSchema()
        schema.load(content)
        content['id'] = self.restaurants[len(self.restaurants) - 1]['id'] + 1
        self.restaurants.append(content)
        return jsonify(self.restaurants), 201


class RestaurantItemEndpoint(MethodView):
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def get(self, restaurant_id):
        for restaurant in self.restaurants:

            if restaurant["id"] == restaurant_id:
                return jsonify(restaurant), 200
        raise WrongIdError(description="Restaurant with such ID doesn't exist")

    def put(self, restaurant_id):
        content = request.json
        schema = RestaurantCreateOrUpdateSchema(partial=True)
        schema.load(content)
        for restaurant in self.restaurants:
            if restaurant["id"] == restaurant_id:
                for key, value in content.items():
                    restaurant[key] = value
                return jsonify(restaurant), 200
        raise WrongIdError(description="No restaurant to update. Restaurant with such ID doesn't exist")


def handle_validation_error(ex):
    return jsonify({
        "name": "Bad Request",
        "description": ex.messages
    }), 400


def handle_exception(ex):
    return jsonify({
        "name": ex.name,
        "description": ex.description
    }), ex.status_code


def handle_standard_exception(ex):
    return jsonify({
        "code": ex.code,
        "name": ex.name,
        "description": ex.description,
    }), ex.code


def register_url_rules(app, restaurants):
    app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api", restaurants))
    app.add_url_rule("/api/restaurants/<int:restaurant_id>",
                     view_func=RestaurantItemEndpoint.as_view("restaurant_item_api", restaurants))


def register_error_handlers(app):
    app.register_error_handler(CustomError, handle_exception)
    app.register_error_handler(HTTPException, handle_standard_exception)
    app.register_error_handler(ValidationError, handle_validation_error)


def create_app():
    application = Flask(__name__)
    application.config.from_object('config.Config')
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        application.config.from_object('config.DevConfig')
    else:
        os.environ['FLASK_ENV'] = 'production'
        application.config.from_object('config.ProdConfig')
    application.config['SWAGGER'] = {
        "uiversion": 3,
        "openapi": "3.0.3",
        'title': 'Delivery System API',
        'description': 'Documentation for Delivery App by Varvara M.',
        'doc_dir': './apidocs/'
    }
    Swagger(application)
    path = application.config.get('PATH_FOR_INITIAL_DATA', 'restaurants.json')
    try:
        with open(path, "r") as read_file:
            data = json.load(read_file)
    except TypeError:
        raise TypeError("Set environment variable: PATH_FOR_INITIAL_DATA")
    register_url_rules(application, data['restaurants'])
    register_error_handlers(application)
    return application


app = create_app()


if __name__ == '__main__':
    app.run(app.config.get("HOST"), port=int(app.config.get("PORT", 5000)))

