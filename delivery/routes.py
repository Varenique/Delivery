from flask import jsonify, request
from flask.views import MethodView
from flask import Response
from delivery.models import Restaurant


class RestaurantEndpoint(MethodView):
    def __init__(self, restaurants, schema):
        self.restaurants = restaurants
        self.schema = schema

    def get(self):
        return Response(self.restaurants.get_all(), mimetype="application/json", status=200)

    def post(self):
        content = request.json
        self.restaurants.create(self.schema.load(content))
        return Response(self.restaurants.get_all(), mimetype="application/json", status=201)


class RestaurantItemEndpoint(MethodView):
    def __init__(self, restaurants, schema):
        self.restaurants = restaurants
        self.schema = schema

    def get(self, restaurant_id: str):
        return self.schema.dump(self.restaurants.get_by_id(restaurant_id)), 200

    def put(self, restaurant_id: str):
        content = request.json
        restaurant = self.schema.load(content)
        restaurant.id = restaurant_id
        self.restaurants.update(restaurant)
        return jsonify(self.schema.dump(self.restaurants.get_by_id(restaurant_id))), 200
