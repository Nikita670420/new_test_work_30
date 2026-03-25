import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_read_recipes(client):
    """Тест GET /recipes - должен вернуть 200"""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_recipe(client):
    """Тест POST /recipes - создание рецепта"""
    response = client.post("/recipes", json={"name": "Тестовый суп", "cooking_time": 30, "ingredients": ["вода", "картошка"], "description": "Простой суп"})
    assert response.status_code == 201
    assert response.json()["name"] == "Тестовый суп"
