def test_get_nonexisten(test_client, get_mocker):
    response = test_client.get('/api/restaurants/3000')
    assert response.status_code == 404
    assert {"description": "Restaurant with such ID doesn\'t exist", "name": "Not Found"} == response.get_json()


def test_put_nonexisten(test_client, get_mocker):
    response = test_client.put('/api/restaurants/3000', json={"name": "Hotfix"})
    assert response.status_code == 404
    assert {"description": "No restaurant to update. Restaurant with such ID doesn\'t exist",
            "name": "Not Found"} == response.get_json()
    # assert b'{\n  "description": "No restaurant to update. Restaurant with such ID doesn\'t exist", ' \
    #        b'\n  "name": "Not Found"\n}\n' == response.data


def test_get_one(test_client, get_mocker):
    response = test_client.get('/api/restaurants/0')
    data = {"address": "Minsk", "id": 0, "name": "Vasilki", "phone_number": "+375297777777",
            "work_time": "Monday-Sunday: 08:00 - 23:45"}
    assert response.status_code == 200
    assert data == response.get_json()


def test_put_one(test_client, get_mocker):
    data = {"name": "Hotfix"}
    response = test_client.put('/api/restaurants/0', json=data)
    assert response.status_code == 200
    assert data['name'] == response.get_json()['name']
