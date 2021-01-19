def test_put_empty(test_client):
    response = test_client.put('/api/restaurants/0')
    assert response.status_code == 400
    assert b'{\n  "description": "Required data not available(No data)", \n  "name": "Bad request"\n}\n' \
           == response.data


def test_put_wrong_type(test_client):
    response = test_client.put('/api/restaurants/0', json={"name": 5})
    assert response.status_code == 400
    assert b'{\n  "description": "Required data not correct, doesn\'t match format", \n  "name": "Bad request"\n}\n' \
           == response.data


def test_put_wrong_format(test_client):
    response = test_client.put('/api/restaurants/0', json={"namee": "Hotfix"})
    assert response.status_code == 400
    assert b'{\n  "description": "Required data not correct, doesn\'t match format", \n  "name": "Bad request"\n}\n' \
           == response.data


def test_post_empty(test_client):
    response = test_client.post('/api/restaurants')
    assert response.status_code == 400
    assert b'{\n  "description": "Required data not available(No data)", \n  "name": "Bad request"\n}\n' \
           == response.data


def test_post_wrong_format(test_client):
    response = test_client.post('/api/restaurants', json={"address": "Minsk", "id": 5,
                                                          "work_time": "Monday-Sunday: 08:00 - 23:45",
                                                          "phone_number": "+375297777777"})
    assert response.status_code == 400
    assert b'{\n  "description": "Sent data not correct, doesn\'t match format", \n  "name": "Bad request"\n}\n' \
           == response.data


def test_post_wrong_type(test_client):
    response = test_client.post('/api/restaurants', json={"name": "CoffeHouse",
                                                          "address": "Minsk", "id": "7",
                                                          "work_time": "Monday-Sunday: 08:00 - 23:45",
                                                          "phone_number": "+375297777777"})
    assert response.status_code == 400
    assert b'{\n  "description": "Type of sent data not correct", \n  "name": "Bad request"\n}\n' \
           == response.data
