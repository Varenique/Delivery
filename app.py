from flask import Flask, request, jsonify
import json
from flask.views import MethodView


app = Flask(__name__)
with open("restaurants.json", "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


class RestaurantEndpoint(MethodView):
    def get(self):
        return jsonify({'restaurants': restaurants}), 200

    def post(self):
        content = request.json
        if content is not None:
            restaurants[str(len(restaurants))] = content['restaurant_info']
        return jsonify({'restaurants': restaurants}), 201


class RestaurantItemEndpoint(MethodView):
    def get(self, restaurant_id):
        return jsonify({'info': restaurants[str(restaurant_id)]}), 200

    def put(self, restaurant_id):
        content = request.json
        if content is not None:
            restaurants[str(restaurant_id)] = content['restaurant_name']
        return jsonify({'restaurants': restaurants}), 200


app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api"))
app.add_url_rule("/api/restaurants/<int:restaurant_id>", view_func=RestaurantItemEndpoint.as_view("restaurant_item_api"))


if __name__ == '__main__':
    app.run()
