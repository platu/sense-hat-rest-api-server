import pytest
from rest_04 import create_app


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


# Successful POST request only with the "msg" key
def test_successful_msg_post(client):
    response = client.post('/api/v1/messages/',
                           json={"msg": "Hello!"})
    assert response.status_code == 200  # nosec B101
    assert "{\"message\": \"Message processed\"}" in (
        response.data.decode()
    )  # nosec B101


# Successful POST request with "msg" and "speed" keys
def test_successful_msg_speed_post(client):
    response = client.post('/api/v1/messages/',
                           json={
                               "msg": "Hello!",
                               "speed": 0.01
                               })
    assert response.status_code == 200  # nosec B101
    assert "{\"message\": \"Message processed\"}" in (
        response.data.decode()
    )  # nosec B101


# Successful POST request with "msg", "speed", and color keys
def test_successful_msg_speed_colors_post(client):
    response = client.post('/api/v1/messages/',
                           json={
                               "msg": "Hello!",
                               "speed": 0.05,
                               "fg": "[0, 0, 255]",
                               "bg": "[255, 255, 255]"
                               })
    assert response.status_code == 200  # nosec B101
    assert "{\"message\": \"Message processed\"}" in (
        response.data.decode()
    )  # nosec B101


def test_invalid_json(client):
    response = client.post('/api/v1/messages/',
                           data="Invalid JSON")
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid JSON\"}" in (
        response.data.decode()
    )  # nosec B101


def test_missing_msg_key(client):
    response = client.post('/api/v1/messages/',
                           json={"Invalid key": "Hello!"})
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Missing \'msg\' key\"}" in (
        response.data.decode()
    )  # nosec B101


def test_invalid_speed_value(client):
    response = client.post('/api/v1/messages/',
                           json={"msg": "Hello",
                                 "speed": "invalid"})
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid speed value\"}" in (
        response.data.decode()
    )  # nosec B101


def test_invalid_json_for_fg_and_bg(client):
    response = client.post('/api/v1/messages/',
                           json={"msg": "Hello",
                                 "speed": "0.05",
                                 "fg": "invalid", "bg": "invalid"})
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid JSON for fg or bg\"}" in (
        response.data.decode()
    )  # nosec B101


def test_invalid_color_list_for_fg_and_bg(client):
    response = client.post('/api/v1/messages/',
                           json={"msg": "Hello",
                                 "speed": "0.05",
                                 "fg": "[0, 128]", "bg": "[0, 0, 0]"})
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid color type\"}" in (
        response.data.decode()
    )  # nosec B101


def test_invalid_color_value_for_fg_and_bg(client):
    response = client.post('/api/v1/messages/',
                           json={"msg": "Hello",
                                 "speed": "0.05",
                                 "fg": "[256, 0, 0]", "bg": "[0, 256, 0]"})
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid color value\"}" in (
        response.data.decode()
    )  # nosec B101


def test_invalid_JSON_keys(client):
    response = client.post('/api/v1/messages/',
                           json={"msg": "Hello",
                                 "fg": "[255, 0, 0]", "bg": "[0, 255, 0]"})
    assert response.status_code == 400  # nosec B101
    assert "{\"error\": \"Invalid JSON\"}" in (
        response.data.decode()
    )  # nosec B101
