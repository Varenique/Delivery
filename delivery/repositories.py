from abc import ABC, abstractmethod
from delivery.error_handling import WrongIdError
from delivery.models import Restaurant


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
    def create(self, content: Restaurant) -> None:
        content.save()

    def update(self, content: Restaurant) -> None:
        new_data = content.to_json()
        Restaurant.objects(id=content.id).update_one(**new_data)

    def get_all(self):
        return Restaurant.objects().to_json()

    def get_by_id(self, restaurant_id):
        try:
            return Restaurant.objects.get(pk=restaurant_id)
        except:
            raise WrongIdError(description="Restaurant with such ID doesn't exist")

