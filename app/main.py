from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
import json
import os

app = FastAPI()

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "pokedex.json")
with open(DATA_PATH) as f:
    pokemons = json.load(f)

@app.get("/pokemon/{name}")
def get_pokemon(id: int):
    result = next((poke for poke in pokemons if poke.get("id") == id), None)
    if result:
        return result
    return {"error": "Pokémon not found"}