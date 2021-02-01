def test_get_nonexisten(test_client):
    response = test_client.get('/api/restaurants/3000')
    assert response.status_code == 404
    assert {"description": "Restaurant with such ID doesn\'t exist", "name": "Not Found"} == response.get_json()


def test_put_nonexisten(test_client):
    response = test_client.put('/api/restaurants/3000', json={"name": "Hotfix"})
    assert response.status_code == 404
    assert {"description": "No restaurant to update. Restaurant with such ID doesn\'t exist",
            "name": "Not Found"} == response.get_json()


def test_get_one(test_client, all_restaurants):
    response = test_client.get('/api/restaurants/0')
    assert response.status_code == 200
    assert all_restaurants[0] == response.get_json()


def test_put(test_client):
    data = {"name": "Hotfix"}
    response = test_client.put('/api/restaurants/0', json=data)
    assert response.status_code == 200
    assert data['name'] == response.get_json()['name']
