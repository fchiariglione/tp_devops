from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging
import json
import os

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

REQUEST_COUNT = Counter(
    'pokemon_requests_total', 'Total HTTP requests for pokemon endpoint', ['method', 'endpoint', 'status_code']
)
REQUEST_LATENCY = Histogram(
    'pokemon_request_latency_seconds', 'Latency of pokemon endpoint', ['endpoint']
)

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "pokedex.json")
with open(DATA_PATH) as f:
    pokemons = json.load(f)

@app.get("/pokemon/{name}")
def get_pokemon(name: str):
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
def get_pokemon(id: int):
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
        logging.warning(f"Pokemon {id} not found")
        logging.info(f"End request for /pokedex/{id} with 404")
        raise HTTPException(status_code=404, detail="Pokemon not found")

@app.get('/metrics')
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
