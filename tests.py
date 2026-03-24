import pytest
from main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI" in response.text

def test_create_item(client):
    response = client.post("/items/", json={"name": "test", "price": 10})
    assert response.status_code == 200
    assert response.json()["name"] == "test"
