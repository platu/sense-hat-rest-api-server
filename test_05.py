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
