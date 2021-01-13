from flask import Flask, request, jsonify
import json
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
        if len(restaurants) <= restaurant_id:
            raise(HandledError(status_code=404, description="Page doesn't exist", name="Not Found"))
        return jsonify(restaurants[restaurant_id]), 200

    def put(self, restaurant_id):
        content = request.json
        answer = 200
        if content is None:
            raise HandledError(status_code=400, description="Required data not available", name="Bad Request")
        if len(restaurants) <= restaurant_id:
            answer = 201
            restaurants.append(content)
        else:
            restaurants[restaurant_id] = content
        return jsonify(restaurants[restaurant_id]), answer


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
