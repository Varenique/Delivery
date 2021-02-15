def test_login_and_get_user(test_client):
    data = {"login": "varya", "password": "1234"}
    response = test_client.post('api/login', json=data)
    assert response.status_code == 200
    assert "access_token" in response.get_json().keys()

    response = test_client.get('api/login', headers={"Authorization": "Bearer {}".format(response.get_json()["access_token"])})
    assert response.get_json() == {"id": "0",
                                   "name": "Varvara",
                                   "phone_number": "+375334567890",
                                   "login": "varya",
                                   "role": "user"}


def test_register_user(test_client):
    data = {"login": "some", "name": "Person", "phone_number": "+375334567890", "role": "user", "password": "2222"}
    response = test_client.post('api/register', json=data)
    data.pop("password")
    assert response.status_code == 201
    assert response.get_json() == data


