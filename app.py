import json
from flask import Flask, request, jsonify
from flask.views import MethodView
from HandledError import HandledError

app = Flask(__name__)
with open("restaurants.json", "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


class RestaurantEndpoint(MethodView):
    def get(self):
        return jsonify(restaurants), 200

    def post(self):
        content = request.json
        if content is None:
            raise(HandledError(status_code=400, description="Required data not available", name="Bad Request"))
        restaurants.append(content)
        return jsonify({'restaurants': restaurants}), 201


class RestaurantItemEndpoint(MethodView):
    def get(self, restaurant_id):
        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return jsonify(restaurant), 200
        raise(HandledError(status_code=404, description="Page doesn't exist", name="Not Found"))

    def put(self, restaurant_id):
        content = request.json
        if content is None:
            raise HandledError(status_code=400, description="Required data not available", name="Bad Request")
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


if __name__ == '__main__':
    app.run()










