def test_get_restaurants(test_client):
    response = test_client.get('/api/restaurants')
    assert response.status_code == 200
    assert b'[{"address":"Minsk","id":0,"name":"Vasilki","phone_number":"+375297777777",' \
           b'"work_time":"Monday-Sunday: 08:00 - 23:45"},{"address":"Minsk","id":1,"name":"Mama Doma",' \
           b'"phone_number":"+375336666666","work_time":"Monday-Sunday: 10:00 - 22:00"},{"address":"Minsk",' \
           b'"id":2,"name":"Sorso","phone_number":"+375290101111","work_time":"Monday-Sunday: 09:30 - 23:00"},' \
           b'{"address":"Minsk","id":3,"name":"Gan bei","phone_number":"+375258181888",' \
           b'"work_time":"Monday-Sunday: 8:30 - 22:45"},{"address":"Minsk","id":4,"name":"KFC",' \
           b'"phone_number":"+375295678312","work_time":"Monday-Sunday: 08:00 - 23:00"}]\n' == response.data
