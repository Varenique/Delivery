import pytest
from delivery.app import create_app
from delivery.schemas import RestaurantCreateOrUpdateSchema
from delivery.models import Restaurant
from delivery.repositories import MemoryRestaurantRepository


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture()
def all_restaurants():

    return [{"address": "Minsk", "id": '0', "name": "Vasilki", "phone_number": "+375297777777",
             "work_time": "Monday-Sunday: 08:00 - 23:45"},
            {"address": "Minsk", "id": '1', "name": "Mama Doma", "phone_number": "+375336666666",
             "work_time": "Monday-Sunday: 10:00 - 22:00"}]


@pytest.fixture(autouse=True)
def mocker_restaurant_endpoint(mocker, all_restaurants):
    first = Restaurant("Vasilki", "Minsk", "Monday-Sunday: 08:00 - 23:45", "+375297777777", '0')
    second = Restaurant("Mama Doma", "Minsk", "Monday-Sunday: 10:00 - 22:00", "+375336666666", '1')
    new_repo = MemoryRestaurantRepository([first, second])

    def new_init(self, restaurants, schema):
        self.restaurants = new_repo
        self.schema = RestaurantCreateOrUpdateSchema()
    yield mocker.patch('delivery.routes.RestaurantEndpoint.__init__', new_init)


@pytest.fixture(autouse=True)
def mocker_restaurant_item_endpoint(mocker, all_restaurants):
    first = Restaurant("Vasilki", "Minsk", "Monday-Sunday: 08:00 - 23:45", "+375297777777", '0')
    second = Restaurant("Mama Doma", "Minsk", "Monday-Sunday: 10:00 - 22:00", "+375336666666", '1')
    new_repo = MemoryRestaurantRepository([first, second])

    def new_init(self, restaurants, schema):
        self.restaurants = new_repo
        self.schema = RestaurantCreateOrUpdateSchema(partial=True)
    yield mocker.patch('delivery.routes.RestaurantItemEndpoint.__init__', new_init)
