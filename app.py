import json
from flask import Flask, request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import HTTPException
from error_handling import HandledError, ValidationError

app = Flask(__name__)
pattern = {'id': int, 'name': str, 'address': str, "work_time": str, "phone_number": str}
with open("restaurants.json", "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


def validate_post(content):
    if content is None:
        raise ValidationError(description="Required data not available(No data)")
    if content.keys() != pattern.keys():
        raise ValidationError(description="Sent data not correct, doesn't match format")
    for key, value in pattern.items():
        if type(content[key]) != value:
            raise ValidationError(description="Type of sent data not correct")


def validate_put(content):
    if content is None:
        raise ValidationError(description="Required data not available(No data)")
    for key in content.keys():
        if key not in pattern.keys():
            raise ValidationError(description="Required data not correct, doesn't match format")


class RestaurantEndpoint(MethodView):
    def get(self):
        return jsonify(restaurants), 200

    def post(self):
        content = request.json
        validate_post(content)
        restaurants.append(content)
        return jsonify(restaurants), 201


class RestaurantItemEndpoint(MethodView):
    def get(self, restaurant_id):
        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return jsonify(restaurant), 200
        raise HandledError(status_code=404, description="Restaurant with such ID doesn't exist", name="Not Found")

    def put(self, restaurant_id):
        content = request.json
        validate_put(content)
        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                for key, value in content.items():
                    restaurant[key] = value
                return jsonify(restaurant), 200
        raise HandledError(status_code=404,
                           description="No restaurant to update. Restaurant with such ID doesn't exist",
                           name="Not Found")


app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api"))
app.add_url_rule("/api/restaurants/<int:restaurant_id>", view_func=RestaurantItemEndpoint.as_view("restaurant_item_api"))


@app.errorhandler(HandledError)
def handle_exception(ex):
    return jsonify({
        "name": ex.name,
        "description": ex.description
    }), ex.status_code


@app.errorhandler(HTTPException)
def handle_standard_exception(ex):
    return jsonify({
        "code": ex.code,
        "name": ex.name,
        "description": ex.description,
    }), ex.code


if __name__ == '__main__':
    app.run()
