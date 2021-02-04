from abc import ABC, abstractmethod
from delivery.error_handling import WrongIdError
from delivery.models import Restaurant
from typing import Iterable


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
        content.id = len(self.restaurants)
        self.restaurants.append(content)

    def update(self, content: Restaurant) -> None:
        for restaurant in self.restaurants:
            if restaurant.id == content.id:
                for key in ["name", "address", "work_time", "phone_number"]:
                    if getattr(content, key) != "":
                        setattr(restaurant, key, getattr(content, key))
                return
        raise WrongIdError(description="Restaurant with such ID doesn't exist")

    def get_all(self) -> Iterable[Restaurant]:
        return self.restaurants

    def get_by_id(self, restaurant_id: int) -> Restaurant:
        for restaurant in self.restaurants:
            if restaurant.id == restaurant_id:
                return restaurant
        raise WrongIdError(description="Restaurant with such ID doesn't exist")
