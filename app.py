from flask import Flask, request, jsonify
import json
from flask.views import MethodView
from werkzeug.routing import ValidationError

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
            raise ValidationError
        restaurants.append(content)
        return jsonify({'restaurants': restaurants}), 201


class RestaurantItemEndpoint(MethodView):
    def get(self, restaurant_id):
        return jsonify(restaurants[restaurant_id]), 200

    def put(self, restaurant_id):
        content = request.json
        answer = 200
        if content is not None:
            if len(restaurants) <= restaurant_id:
                answer = 201
                restaurants.append(content)
            else:
                restaurants[restaurant_id] = content
        return jsonify(restaurants[restaurant_id]), answer


app.add_url_rule("/api/restaurants", view_func=RestaurantEndpoint.as_view("restaurant_api"))
app.add_url_rule("/api/restaurants/<int:restaurant_id>", view_func=RestaurantItemEndpoint.as_view("restaurant_item_api"))


if __name__ == '__main__':
    app.run()
