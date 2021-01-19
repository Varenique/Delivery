import os
import json


def test_get_nonexisten(test_client):
    response = test_client.get('/api/restaurants/3000')
    assert response.status_code == 404
    assert b'{\n  "description": "Restaurant with such ID doesn\'t exist", \n  "name": "Not Found"\n}\n' \
           == response.data


def test_put_nonexisten(test_client):
    response = test_client.put('/api/restaurants/3000', json={"name": "Hotfix"})
    assert response.status_code == 404
    assert b'{\n  "description": "No restaurant to update. Restaurant with such ID doesn\'t exist", ' \
           b'\n  "name": "Not Found"\n}\n'  == response.data


def test_get_one(test_client):
    response = test_client.get('/api/restaurants/0')
    path = os.environ.get('PATH_FOR_INITIAL_DATA', 'restaurants.json')
    with open(path, "r") as read_file:
        data = json.load(read_file)['restaurants'][0]
    assert response.status_code == 200
    assert b'data in response.data'


def test_put_one(test_client):
    data = {"name": "Hotfix"}
    response = test_client.put('/api/restaurants/0', json=data)
    assert response.status_code == 200
    assert b'data in response.data'
