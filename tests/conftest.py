import pytest
from app import create_app


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


@pytest.fixture(autouse=True)
def mocker_get_all(mocker, all_restaurants):
    def new_get_all(self):
        return all_restaurants
    yield mocker.patch('app.MemoryRestaurantRepository.get_all', new_get_all)


@pytest.fixture(autouse=True)
def mocker_get_by_id(mocker, all_restaurants):
    def new_get_by_id(self, restaurant_id):
        return all_restaurants[restaurant_id]
    yield mocker.patch('app.MemoryRestaurantRepository.get_by_id', new_get_by_id)


@pytest.fixture(autouse=True)
def mocker_save(mocker, all_restaurants):
    def new_save(self, content, restaurant_id=None):
        if restaurant_id is None or restaurant_id >= len(all_restaurants):
            all_restaurants.append(content)
        else:
            for key, value in content.items():
                all_restaurants[restaurant_id][key] = value
    yield mocker.patch('app.MemoryRestaurantRepository.save', new_save)
