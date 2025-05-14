from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_existing_pokemon():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    data = response.json()
    assert data["name"]["english"] == "Pikachu"


def test_get_nonexistent_pokemon():
    response = client.get("/pokemon/goku")
    assert response.status_code == 404

def test_get_existing_pokedex():
    response = client.get("/pokedex/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_nonexistent_pokedex():
    response = client.get("/pokemon/9999")
    assert response.status_code == 404

def test_create_new_pokemon():
    new_pokemon = {
        "id": 999,
        "name": {
            "english": "Testmon",
            "japanese": "テストモン",
            "chinese": "测试怪",
            "french": "Testmon"
        },
        "type": ["Test"],
        "base": {
            "HP": 100,
            "Attack": 80,
            "Defense": 70,
            "Sp. Attack": 90,
            "Sp. Defense": 85,
            "Speed": 60
        },
        "species": "Test Pokémon",
        "description": "A test Pokémon used for API testing.",
        "evolution": { "next": [["1000", "Level 50"]] },
        "profile": {
            "height": "1.0 m",
            "weight": "10.0 kg",
            "egg": ["Monster", "Test"],
            "ability": [["Test Boost", "false"], ["Hidden Power", "true"]],
            "gender": "50:50"
        },
        "image": {
            "sprite": "https://example.com/sprite.png",
            "thumbnail": "https://example.com/thumbnail.png",
            "hires": "https://example.com/hires.png"
        }
    }

    response = client.post("/pokemon", json=new_pokemon)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 999
    assert data["name"]["english"] == "Testmon"
    assert data["base"]["HP"] == 100