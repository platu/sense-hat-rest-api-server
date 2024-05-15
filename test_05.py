import json
import pytest
from rest_05 import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


# 1. Successful DELETE request without color data
def test_successful_delete(client):
    response = client.delete('/api/v1/leds/')
    assert response.status_code == 200  # nosec B101
    assert "{\"message\": \"LEDs cleared\"}" in (
        response.data.decode()
    )  # nosec B101


# 2. Successful DELETE request with color data
def test_successful_delete_with_color(client):
    response = client.delete('/api/v1/leds/',
                             json={"color": [0, 64, 0]}
                             )
    assert response.status_code == 200  # nosec B101
    assert "{\"message\": \"LEDs cleared\"}" in (
        response.data.decode()
    )  # nosec B101


# 3. Failed DELETE request with invalid JSON
def test_failed_delete_invalid_json(client):
    response = client.delete('/api/v1/leds/',
                             data="invalid json"
                             )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid JSON\"}" in (
        response.data.decode()
    )  # nosec B101


# 4. Failed DELETE request with invalid color
def test_failed_delete_invalid_color(client):
    response = client.delete('/api/v1/leds/',
                             json={"color": "invalid color"}
                             )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid color\"}" in (
        response.data.decode()
    )  # nosec B101


# 5. Failed DELETE request with invalid color value
def test_failed_delete_invalid_color_value(client):
    response = client.delete('/api/v1/leds/',
                             json={"color": [0, 64, 256]}
                             )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid color value\"}" in (
        response.data.decode()
    )  # nosec B101


# 6. Successful GET request
def test_successful_get(client):
    response = client.get('/api/v1/leds/')
    assert response.status_code == 200  # nosec B101
    data = json.loads(response.data.decode())
    assert isinstance(data["leds"], list)  # nosec B101
    assert len(data["leds"]) == 64  # nosec B101
    assert all(isinstance(color, list) for color in data["leds"])  # nosec B101


# 7. Successful POST request
def test_successful_post(client):
    f = open("pixelart/yoda.json", "r")
    data = json.loads(f.read())
    response = client.post('/api/v1/leds/',
                           json=data
                           )
    assert response.status_code == 200  # nosec B101
    assert "{\"message\": \"LEDs updated\"}" in (
        response.data.decode()
    )  # nosec B101


# 8. Failed POST request with invalid JSON
def test_failed_post_invalid_json(client):
    response = client.post('/api/v1/leds/',
                           data="invalid json"
                           )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid JSON\"}" in (
        response.data.decode()
    )  # nosec B101


# 9. Failed POST request with missing 'leds' key
def test_failed_post_missing_leds(client):
    response = client.post('/api/v1/leds/',
                           json={"notleds": "missing"}
                           )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Missing 'leds' key\"}" in (
        response.data.decode()
    )  # nosec B101


# 10. Failed POST request with invalid color value
def test_failed_post_invalid_color(client):
    response = client.post('/api/v1/leds/',
                           json={"leds": [[0, 0, 96], [47, 68, 256]]}
                           )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid color value\"}" in (
        response.data.decode()
    )  # nosec B101


# 11. Failed POST request with invalid color matrix size
def test_failed_post_invalid_color_matrix_size(client):
    response = client.post('/api/v1/leds/',
                           json={"leds": [[0, 0, 96], [47, 68, 255]]}
                           )
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid color matrix size\"}" in (
        response.data.decode()
    )  # nosec B101
