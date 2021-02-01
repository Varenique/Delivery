import pytest
from delivery.app import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture()
def all_restaurants():
    return [{"address": "Minsk", "id": 0, "name": "Vasilki", "phone_number": "+375297777777",
                             "work_time": "Monday-Sunday: 08:00 - 23:45"},
                            {"address": "Minsk", "id": 1, "name": "Mama Doma", "phone_number": "+375336666666",
                             "work_time": "Monday-Sunday: 10:00 - 22:00"}]


@pytest.fixture()
def mocker_restaurant_endpoint(mocker, all_restaurants):
    def new_init(self, restaurants):
        self.restaurants = all_restaurants
    yield mocker.patch('delivery.app.RestaurantEndpoint.__init__', new_init)


@pytest.fixture()
def mocker_restaurant_item_endpoint(mocker, all_restaurants):
    def new_init(self, restaurants):
        self.restaurants = all_restaurants

    yield mocker.patch('delivery.app.RestaurantItemEndpoint.__init__', new_init)

