from abc import ABC, abstractmethod
from delivery.error_handling import WrongIdError


class AbstractRestaurantRepository(ABC):
    @abstractmethod
    def create(self, content):
        pass

    @abstractmethod
    def update(self, content, restaurant_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass


class MemoryRestaurantRepository(AbstractRestaurantRepository):
    restaurants = []
    # def __init__(self, restaurants=None):
    #     self.restaurants = restaurants or []

    def create(self, content):
        content.id = len(self.restaurants)
        self.restaurants.append(content)

    def update(self, content_dictionary, restaurant_id):
        for restaurant in self.restaurants:
            if restaurant.id == restaurant_id:
                for key, value in content_dictionary.items():
                    setattr(restaurant, key, value)
                return
        raise WrongIdError(description="Restaurant with such ID doesn't exist")

    def get_all(self):
        return self.restaurants

    def get_by_id(self, restaurant_id):
        for restaurant in self.restaurants:
            if restaurant.id == restaurant_id:
                return restaurant
        raise WrongIdError(description="Restaurant with such ID doesn't exist")
