import pytest
from fastapi.testclient import TestClient
from portfolio_research.interfaces.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_signup_validation_error(client):
    # Missing email
    response = client.post("/api/v1/auth/signup", json={"username": "testuser", "password": "123"})
    assert response.status_code == 422  # Pydantic validation error


def test_login_validation_error(client):
    response = client.post("/api/v1/auth/login", json={"username": ""})
    assert response.status_code == 422
