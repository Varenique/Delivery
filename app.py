import json
import os
from flask import Flask, request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import HTTPException
from flasgger import Swagger, swag_from
from error_handling import CustomError, ValidationError, WrongIdError


path = os.environ.get('PATH_FOR_INITIAL_DATA', 'restaurants.json')
with open(path, "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


class Validation:
    pattern = {'id': int, 'name': str, 'address': str, "work_time": str, "phone_number": str}

    @staticmethod
    def empty(content):
        if content is None:
            raise ValidationError(description="Required data not available(No data)")

    def put_validation(self, content):
        self.empty(content)
        for key in content.keys():
            if key not in self.pattern.keys() or type(content[key]) != self.pattern[key]:
                raise ValidationError(description="Required data not correct, doesn't match format")

    def post_validation(self, content):
        self.empty(content)
        if content.keys() != self.pattern.keys():
            raise ValidationError(description="Sent data not correct, doesn't match format")
        for key, value in self.pattern.items():
            if type(content[key]) != value:
                raise ValidationError(description="Type of sent data not correct")


validation = Validation()


class RestaurantEndpoint(MethodView):
    @swag_from("yaml\\restaurants.yml")
    def get(self):
        return jsonify(restaurants), 200

    @swag_from("yaml\\restaurants.yml")
    def post(self):
        content = request.json
        validation.post_validation(content)
        restaurants.append(content)
        return jsonify(restaurants), 201


class RestaurantItemEndpoint(MethodView):
    @swag_from("yaml\\restaurant_item.yml")
    def get(self, restaurant_id):

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return jsonify(restaurant), 200
        raise WrongIdError(description="Restaurant with such ID doesn't exist")

    @swag_from("yaml\\restaurant_item.yml")
    def put(self, restaurant_id):
        content = request.json
        validation.put_validation(content)
        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                for key, value in content.items():
                    restaurant[key] = value
                return jsonify(restaurant), 200
        raise WrongIdError(description="No restaurant to update. Restaurant with such ID doesn't exist")


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


def register_url_rules(app):
    app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api"))
    app.add_url_rule("/api/restaurants/<int:restaurant_id>",
                     view_func=RestaurantItemEndpoint.as_view("restaurant_item_api"))
    app.register_error_handler(CustomError, handle_exception)
    app.register_error_handler(HTTPException, handle_standard_exception)


def create_app():
    application = Flask(__name__)
    application.config.from_object('config.Config')
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        application.config.from_object('config.DevConfig')
    else:
        os.environ['FLASK_ENV'] = 'production'
        application.config.from_object('config.ProdConfig')
    register_url_rules(application)
    Swagger(application)
    return application


app = create_app()

if __name__ == '__main__':
    app.run()

