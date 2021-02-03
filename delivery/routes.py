from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from delivery.repositories import AbstractRestaurantRepository


class RestaurantEndpoint(MethodView):
    def __init__(self, restaurants: AbstractRestaurantRepository, schema):
        self.restaurants = restaurants
        self.schema = schema

    def get(self):
        return jsonify([self.schema.dump(restaurant) for restaurant in self.restaurants.get_all()]), 200

    def post(self):
        content = request.json
        self.restaurants.create(self.schema.load(content))
        return jsonify([self.schema.dump(restaurant) for restaurant in self.restaurants.get_all()]), 201


class RestaurantItemEndpoint(MethodView):
    def __init__(self, restaurants: AbstractRestaurantRepository, schema):
        self.restaurants = restaurants
        self.schema = schema

    def get(self, restaurant_id: int):
        return jsonify(self.schema.dump(self.restaurants.get_by_id(restaurant_id))), 200

    def put(self, restaurant_id: int):
        content = request.json
        restaurant = self.schema.load(content)
        restaurant.id = restaurant_id
        self.restaurants.update(restaurant)
        return jsonify(self.schema.dump(self.restaurants.get_by_id(restaurant_id))), 200
