from abc import ABC, abstractmethod
from delivery.error_handling import WrongIdError
from delivery.models import Restaurant
from typing import Iterable
from bson.objectid import ObjectId
from dataclasses import asdict
from pymongo import MongoClient, ReturnDocument


class AbstractRestaurantRepository(ABC):
    @abstractmethod
    def create(self, content: Restaurant) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, content: Restaurant) -> Restaurant:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Iterable[Restaurant]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, restaurant_id) -> Restaurant:
        raise NotImplementedError


class MemoryRestaurantRepository(AbstractRestaurantRepository):
    def __init__(self, restaurants=None):
        self.restaurants = restaurants or []

    def create(self, content: Restaurant) -> None:
        content.id = str(len(self.restaurants))
        self.restaurants.append(content)

    def update(self, content: Restaurant) -> Restaurant:
        for restaurant in self.restaurants:
            if restaurant.id == content.id:
                for key in ["name", "address", "work_time", "phone_number"]:
                    if getattr(content, key) != "":
                        setattr(restaurant, key, getattr(content, key))
                return Restaurant
        raise WrongIdError(description="Restaurant with such ID doesn't exist")

    def get_all(self) -> Iterable[Restaurant]:
        return self.restaurants

    def get_by_id(self, restaurant_id: str) -> Restaurant:
        for restaurant in self.restaurants:
            if restaurant.id == restaurant_id:
                return restaurant
        raise WrongIdError(description="Restaurant with such ID doesn't exist")


class MongoRestaurantRepository(AbstractRestaurantRepository):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client.restaurants

    def create(self, content: Restaurant) -> None:
        content = asdict(content)
        content.pop("id")
        self.mongo_client.insert_one(content)

    def update(self, content: Restaurant) -> Restaurant:
        update_data = asdict(content)
        restaurant_id = {'_id': ObjectId(update_data["id"])}
        for key, value in asdict(content).items():
            if value == "" or key == "id":
                update_data.pop(key)
        restaurant = self.mongo_client.find_one_and_update(restaurant_id, {"$set": update_data}, return_document=ReturnDocument.AFTER)
        if restaurant is None:
            raise WrongIdError(description="Restaurant with such ID doesn't exist")
        restaurant["id"] = restaurant.pop("_id")
        return Restaurant(**restaurant)

    def get_all(self) -> Iterable[Restaurant]:
        restaurants_list = []
        for restaurant in self.mongo_client.find({}):
            restaurant["id"] = restaurant.pop("_id")
            restaurants_list.append(Restaurant(**restaurant))
        return restaurants_list

    def get_by_id(self, restaurant_id) -> Restaurant:
        restaurant = self.mongo_client.find_one({"_id": ObjectId(restaurant_id)})
        try:
            restaurant["id"] = restaurant.pop("_id")
        except AttributeError:
            raise WrongIdError(description="Restaurant with such ID doesn't exist")
        return Restaurant(**restaurant)


