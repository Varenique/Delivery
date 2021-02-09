def test_get_all(test_client, all_restaurants):
    response = test_client.get('api/restaurants')
    assert response.status_code == 200
    assert all_restaurants == response.get_json()


def test_post(test_client):
    data = {"name": "CoffeHouse", "address": "Minsk", "work_time": "Monday-Sunday: 08:00 - 23:45",
            "phone_number": "+375297777777"}
    response = test_client.post('api/restaurants', json=data)
    last_element = len(response.get_json()) - 1
    assert response.status_code == 201
    assert all([value == response.get_json()[key] for key, value in data.items()])




