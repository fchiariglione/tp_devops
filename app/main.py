from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple, Union
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging
import json
import os

app = FastAPI()

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

REQUEST_COUNT = Counter(
    'pokemon_requests_total', 'Total HTTP requests for pokemon endpoint', ['method', 'endpoint', 'status_code']
)
REQUEST_LATENCY = Histogram(
    'pokemon_request_latency_seconds', 'Latency of pokemon endpoint', ['endpoint']
)

# === Models ===
class PokemonName(BaseModel):
    english: str
    japanese: str
    chinese: str
    french: str


class PokemonStats(BaseModel):
    HP: int
    Attack: int
    Defense: int
    Sp_Attack: int = Field(..., alias="Sp. Attack")
    Sp_Defense: int = Field(..., alias="Sp. Defense")
    Speed: int


class PokemonEvolution(BaseModel):
    next: List[List[Union[str, int]]]


class PokemonProfile(BaseModel):
    height: str
    weight: str
    egg: List[str]
    ability: List[List[Union[str, str]]]
    gender: str


class PokemonImage(BaseModel):
    sprite: str
    thumbnail: str
    hires: str


class Pokemon(BaseModel):
    id: int
    name: PokemonName
    type: List[str]
    base: PokemonStats
    species: str | None = None
    description: str | None = None
    evolution: PokemonEvolution | None = None
    profile: PokemonProfile | None = None
    image: PokemonImage | None = None

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "pokedex.json")
with open(DATA_PATH) as f:
    pokemons = json.load(f)

@app.get("/pokemon/{name}")
def get_pokemon_by_name(name: str):
    logging.info(f"Start request for /pokemon/{name}")
    with REQUEST_LATENCY.labels(endpoint='/pokemon').time():
        for p in pokemons:
            if p["name"]["english"].lower() == name.lower():
                REQUEST_COUNT.labels(method='GET', endpoint='/pokemon', status_code='200').inc()
                logging.info(f"Found pokemon {name}")
                response = JSONResponse(content=p)
                logging.info(f"End request for /pokemon/{name} with 200")
                return response
        REQUEST_COUNT.labels(method='GET', endpoint='/pokemon', status_code='404').inc()
        logging.warning(f"Pokemon {name} not found")
        logging.info(f"End request for /pokemon/{name} with 404")
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
@app.get("/pokedex/{id}")
def get_pokemon_by_pokedex_nro(id: int):
    logging.info(f"Start request for /pokedex/{id}")
    with REQUEST_LATENCY.labels(endpoint='/pokedex').time():
        for p in pokemons:
            if p["id"] == id:
                REQUEST_COUNT.labels(method='GET', endpoint='/pokedex', status_code='200').inc()
                logging.info(f"Found pokemon {id}")
                response = JSONResponse(content=p)
                logging.info(f"End request for /pokedex/{id} with 200")
                return response
        REQUEST_COUNT.labels(method='GET', endpoint='/pokedex', status_code='404').inc()
        logging.warning(f"Pokemon Nro {id} not found")
        logging.info(f"End request for /pokedex/{id} with 404")
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
@app.post("/pokemon", response_model=Pokemon, status_code=201)
def create_pokemon(pokemon: Pokemon):
    logging.info("Start request for POST /pokemon")
    with REQUEST_LATENCY.labels(endpoint='/pokemon').time():
        existing_ids = {p["id"] for p in pokemons}
        if pokemon.id in existing_ids:
            REQUEST_COUNT.labels(method='POST', endpoint='/pokemon', status_code='400').inc()
            logging.warning(f"Pokemon ID {pokemon.id} already exists")
            raise HTTPException(status_code=400, detail="Pokemon ID already exists")


        pokemon_dict = pokemon.dict(by_alias=True)
        pokemons.append(pokemon_dict)

        logging.info(f"Pokemon created: {pokemon.name.english}")
        REQUEST_COUNT.labels(method='POST', endpoint='/pokemon', status_code='201').inc()
        return pokemon

@app.get('/metrics')
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
