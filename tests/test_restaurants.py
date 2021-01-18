import os
import json


def test_post(test_client):
    data = {"name": "CoffeHouse", "address": "Minsk",
            "id": 5, "work_time": "Monday-Sunday: 08:00 - 23:45",
            "phone_number": "+375297777777"}
    response = test_client.post('api/restaurants', json=data)
    assert response.status_code == 201
    assert b"data in response.data"


def test_get_all(test_client):
    path = os.environ.get('PATH_FOR_INITIAL_DATA', 'restaurants.json')
    with open(path, "r") as read_file:
        data = json.load(read_file)['restaurants']
    response = test_client.get('api/restaurants')
    assert response.status_code == 200
    assert b"data in response.data"


