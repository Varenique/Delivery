def test_get_all(test_client, mocker_restaurant_endpoint, all_restaurants):
    response = test_client.get('api/restaurants')
    assert response.status_code == 200
    assert all_restaurants == response.get_json()


def test_post(test_client, mocker_restaurant_endpoint):
    data = {"name": "CoffeHouse", "address": "Minsk",
            "id": 5, "work_time": "Monday-Sunday: 08:00 - 23:45",
            "phone_number": "+375297777777"}
    response = test_client.post('api/restaurants', json=data)
    assert response.status_code == 201
    assert (data in response.get_json()) == True





