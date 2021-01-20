def test_get_all(test_client, get_mocker):
    data = [{"address": "Minsk", "id": 0, "name": "Vasilki", "phone_number": "+375297777777",
            "work_time": "Monday-Sunday: 08:00 - 23:45"}, {"address": "Minsk", "id": 1, "name": "Mama Doma",
            "phone_number": "+375336666666", "work_time": "Monday-Sunday: 10:00 - 22:00"}]
    response = test_client.get('api/restaurants')
    assert response.status_code == 200
    assert data == response.get_json()


def test_post(test_client, get_mocker):
    data = {"name": "CoffeHouse", "address": "Minsk",
            "id": 5, "work_time": "Monday-Sunday: 08:00 - 23:45",
            "phone_number": "+375297777777"}
    response = test_client.post('api/restaurants', json=data)
    assert response.status_code == 201
    assert (data in response.get_json()) == True





