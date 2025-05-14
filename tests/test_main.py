from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_existing_pokemon():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "pikachu"


def test_get_nonexistent_pokemon():
    response = client.get("/pokemon/mewtwo")
    assert response.status_code == 404

def test_get_existing_pokedex():
    response = client.get("/pokedex/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_nonexistent_pokedex():
    response = client.get("/pokemon/999")
    assert response.status_code == 404