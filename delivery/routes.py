import base64
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from delivery.repositories import AbstractRestaurantRepository
from delivery.error_handling import WrongPassword
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt


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
    def __init__(self, users, schema):
        self.users = users
        self.schema = schema

    def post(self):
        login = request.json.get('login', None)
        password = request.json.get('password', None)
        user_password = self.users.get_user(login).password.encode()
        if bcrypt.hashpw(password.encode(), user_password) == user_password:
            access_token = create_access_token(identity=login)
            return jsonify(access_token=access_token), 200
        else:
            raise WrongPassword('Wrong login or password')

    @jwt_required
    def get(self):
        user = self.users.get_user(get_jwt_identity())
        return jsonify(self.schema.dump(user)), 200


class RegisterEndpoint(MethodView):
    def __init__(self, users, schema):
        self.users = users
        self.schema = schema

    def post(self):
        content = request.json
        user = self.schema.load(content)
        a = self.users.add_user(user)
        return jsonify(self.schema.dump(a)), 201
