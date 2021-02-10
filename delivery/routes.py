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
        restaurants = [self.schema.dump(restaurant) for restaurant in self.restaurants.get_all()]
        return jsonify(restaurants), 200

    def post(self):
        content = request.json
        restaurant = self.schema.load(content)
        created_restaurant = self.restaurants.create(restaurant)
        return jsonify(self.schema.dump(created_restaurant)), 201


class RestaurantItemEndpoint(MethodView):
    def __init__(self, restaurants: AbstractRestaurantRepository, schema):
        self.restaurants = restaurants
        self.schema = schema

    def get(self, restaurant_id: str):
        restaurant = self.restaurants.get_by_id(restaurant_id)
        return jsonify(self.schema.dump(restaurant)), 200

    def put(self, restaurant_id: int):
        content = request.json
        restaurant = self.schema.load(content)
        restaurant.id = restaurant_id
        updated_restaurant = self.restaurants.update(restaurant)
        return jsonify(self.schema.dump(updated_restaurant)), 200


class LoginEndpoint(MethodView):
    def __init__(self, users):
        self.users = users

    def post(self):
        username = request.json.get('login', None)
        password = request.json.get('password', None)
        user = self.users.get_user(username)
        if user['password'] == password:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
