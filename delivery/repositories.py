from abc import ABC, abstractmethod
from delivery.error_handling import WrongIdError
from delivery.models import Restaurant
from typing import Iterable
from bson.objectid import ObjectId
from dataclasses import dataclass, asdict


class AbstractRestaurantRepository(ABC):
    @abstractmethod
    def create(self, content: Restaurant):
        raise NotImplementedError

    @abstractmethod
    def update(self, content: Restaurant):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, restaurant_id):
        raise NotImplementedError


class MemoryRestaurantRepository(AbstractRestaurantRepository):
    def __init__(self, restaurants=None):
        self.restaurants = restaurants or []

    def create(self, content: Restaurant) -> None:
        content._id = str(len(self.restaurants))
        self.restaurants.append(content)

    def update(self, content: Restaurant) -> None:
        for restaurant in self.restaurants:
            if restaurant._id == content._id:
                for key in ["name", "address", "work_time", "phone_number"]:
                    if getattr(content, key) != "":
                        setattr(restaurant, key, getattr(content, key))
                return
        raise WrongIdError(description="Restaurant with such ID doesn't exist")

    def get_all(self) -> Iterable[Restaurant]:
        return self.restaurants

    def get_by_id(self, restaurant_id: str) -> Restaurant:
        for restaurant in self.restaurants:
            if restaurant._id == restaurant_id:
                return restaurant
        raise WrongIdError(description="Restaurant with such ID doesn't exist")


class MongoRepository(AbstractRestaurantRepository):
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def create(self, content: Restaurant):
        content = asdict(content)
        content.pop("_id")
        self.restaurants.restaurant.insert_one(content)

    def update(self, content: Restaurant):
        update_data = asdict(content)
        try:
            restaurant = {'_id': ObjectId(update_data["_id"])}
        except:
            raise WrongIdError(description="Restaurant with such ID doesn't exist")
        for key, value in asdict(content).items():
            if value == "" or key == "_id":
                update_data.pop(key)
        self.restaurants.restaurant.update_one(restaurant, {"$set": update_data})

    def get_all(self):
        restaurants_list = []
        for restaurant in self.restaurants.restaurant.find({}):
            restaurants_list.append(Restaurant(**restaurant))
        return restaurants_list

    def get_by_id(self, restaurant_id):
        try:
            restaurant = self.restaurants.restaurant.find_one({"_id": ObjectId(restaurant_id)})
            return Restaurant(**restaurant)
        except:
            raise WrongIdError(description="Restaurant with such ID doesn't exist")

