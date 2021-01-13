import json
from flask import Flask, request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import HTTPException
from HandledError import HandledError

app = Flask(__name__)
pattern = {'id': int, 'name': str, 'address': str, "work_time": str, "phone_number": str}
with open("restaurants.json", "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


def validate_post(content):
    if content is None:
        raise HandledError(status_code=400, description="Required data not available", name="Bad Request")
    if content.keys() != pattern.keys():
        raise HandledError(status_code=400, description="Sent data not correct", name="Bad Request")

    if any([type(content['id']) != pattern['id'],
            type(content['name']) != pattern['name'],
            type(content['address']) != pattern['address'],
            type(content['work_time']) != pattern['work_time'],
            type(content['phone_number']) != pattern['phone_number']]):
        raise HandledError(status_code=400, description="Type of data not correct", name="Bad Request")


def validate_put(content):
    if content is None:
        raise HandledError(status_code=400, description="Required data not available", name="Bad Request")
    for key in content.keys():
        if key not in pattern.keys():
            raise HandledError(status_code=400, description="Required data not correct.", name="Bad Request")


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
        raise(HandledError(status_code=404, description="Page doesn't exist", name="Not Found"))

    def put(self, restaurant_id):
        content = request.json
        validate_put(content)
        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                for key, value in content.items():
                    restaurant[key] = value
                return jsonify(restaurant), 200
        raise (HandledError(status_code=404, description="Page doesn't exist", name="Not Found"))


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
