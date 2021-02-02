from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from delivery.repositories import AbstractRestaurantRepository, MemoryRestaurantRepository


class Restaurant:
    def __init__(self, name, address, work_time, phone_number):
        self.id = 0
        self.name = name
        self.address = address
        self.work_time = work_time
        self.phone_number = phone_number


from delivery.schemas import RestaurantCreateOrUpdateSchema


class RestaurantEndpoint(MethodView):
    def __init__(self, restaurants: AbstractRestaurantRepository):
        self.restaurants = restaurants
        self.schema = RestaurantCreateOrUpdateSchema()

    def get(self):
        return jsonify([self.schema.dump(restaurant) for restaurant in self.restaurants.get_all()]), 200

    def post(self):
        content = request.json
        self.restaurants.create(self.schema.load(content))
        return jsonify([self.schema.dump(restaurant) for restaurant in self.restaurants.get_all()]), 201


class RestaurantItemEndpoint(MethodView):
    def __init__(self, restaurants: AbstractRestaurantRepository):
        self.restaurants = restaurants
        self.schema = RestaurantCreateOrUpdateSchema(partial=True)

    def get(self, restaurant_id):
        return jsonify(self.schema.dump(self.restaurants.get_by_id(restaurant_id))), 200

    def put(self, restaurant_id):
        content = request.json
        errors = self.schema.validate(content)
        if errors != {}:
            raise ValidationError(errors)
        self.restaurants.update(content, restaurant_id)
        return jsonify(self.schema.dump(self.restaurants.get_by_id(restaurant_id))), 200
