import pytest


def test_put_empty(test_client, get_mocker):
    response = test_client.put('/api/restaurants/0')
    assert response.status_code == 400
    assert {"description": "Required data not available(No data)", "name": "Bad request"} == response.get_json()


@pytest.mark.parametrize("key, value", [("name", 5), ("namee", "Hotfix")])
def test_put_wrong_type(test_client, get_mocker, key, value):
    response = test_client.put('/api/restaurants/0', json={key: value})
    assert response.status_code == 400
    assert {"description": "Required data not correct, doesn\'t match format",
            "name": "Bad request"} == response.get_json()


def test_post_empty(test_client, get_mocker):
    response = test_client.post('/api/restaurants')
    assert response.status_code == 400
    assert {"description": "Required data not available(No data)", "name": "Bad request"} == response.get_json()


@pytest.mark.parametrize("number, name, description", [(5, "namee", "Sent data not correct, doesn\'t match format"),
                                                       ("a", "name", "Type of sent data not correct")])
def test_post_wrong_format(test_client, get_mocker, number, name, description):
    response = test_client.post('/api/restaurants', json={"address": "Minsk", "id": number,
                                                          "work_time": "Monday-Sunday: 08:00 - 23:45",
                                                          "phone_number": "+375297777777", name: "Vasilki"})
    assert response.status_code == 400
    assert {"description": "{}".format(description), "name": "Bad request"} == response.get_json()
