import bcrypt
from abc import ABC, abstractmethod
from typing import Iterable
from bson.objectid import ObjectId
from dataclasses import asdict
from pymongo import MongoClient, ReturnDocument
from delivery.error_handling import WrongIdError
from delivery.models import Restaurant, User


class AbstractRestaurantRepository(ABC):
    @abstractmethod
    def create(self, content: Restaurant) -> Restaurant:
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

    def create(self, content: Restaurant) -> Restaurant:
        content.id = str(len(self.restaurants))
        self.restaurants.append(content)
        return content

    def update(self, content: Restaurant) -> Restaurant:
        for restaurant in self.restaurants:
            if restaurant.id == content.id:
                for key in ["name", "address", "work_time", "phone_number"]:
                    if getattr(content, key) != "":
                        setattr(restaurant, key, getattr(content, key))
                return restaurant
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

    def create(self, content: Restaurant) -> Restaurant:
        content = asdict(content)
        content.pop("id")
        return self.mongo_client.find_one_and_update({'name': ''},
                                                     {'$set': content},
                                                     upsert=True, return_document=ReturnDocument.AFTER)

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
        if restaurant is None:
            raise WrongIdError(description="Restaurant with such ID doesn't exist")
        restaurant["id"] = restaurant.pop("_id")
        return Restaurant(**restaurant)


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_user(self, login):
        pass

    def add_user(self, login):
        pass


class MongoUserRepository(AbstractUserRepository):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client.users

    def get_user(self, login):
        user = self.mongo_client.find_one({"login": login})
        if user is None:
            raise WrongIdError(description="Wrong login")
        user["id"] = user.pop("_id")
        return User(**user)

    def add_user(self, content: User):
        password = bcrypt.hashpw(content.password.encode(), bcrypt.gensalt())
        content = asdict(content)
        content.pop("id")
        content['password'] = password.decode()
        return self.mongo_client.find_one_and_update({'name': ''},
                                                     {'$set': content},
                                                     upsert=True, return_document=ReturnDocument.AFTER)


class MemoryUserRepository(AbstractUserRepository):
    def __init__(self, users=None):
        self.users = users or []

    def get_user(self, login):
        for user in self.users:
            if user.login == login:
                return user
        raise WrongIdError(description="Wrong login")

    def add_user(self, content: User):
        password = bcrypt.hashpw(content.password.encode(), bcrypt.gensalt())
        content.password = password.decode()
        content.id = str(len(self.users))
        self.users.append(content)
        return content
