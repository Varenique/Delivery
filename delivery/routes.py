from flask import jsonify, request
from flask.views import MethodView
from delivery.repositories import AbstractRestaurantRepository
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


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


class LoginEndpoint(MethodView):
    def __init__(self, users: AbstractRestaurantRepository, schema):
        self.users = users
        self.schema = schema

    def get(self, restaurant_id: int):
        return jsonify(self.schema.dump(self.restaurants.get_by_id(restaurant_id))), 200

    def post(self):
        username = request.json.get('name', None)
        password = request.json.get('password', None)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
