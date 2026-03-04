import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200


@patch("app.get_connection")
def test_api_data(mock_db, client):
    mock_cursor = mock_db.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, "device_1", 25.5, 60.0, "2026-01-01")
    ]

    response = client.get("/api/data")
    assert response.status_code == 200


@patch("app.get_connection")
def test_db_failure(mock_db, client):
    mock_db.side_effect = Exception("DB Down")

    response = client.get("/api/data")
    assert response.status_code == 500