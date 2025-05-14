# TP DevOps FastAPI Pokedex

## Requirements

- Docker & Docker Compose
- kubectl & kind (or minikube)

## Swagger

- http://localhost:8000/docs

## Local Docker Development

1. From the project root, run Docker Compose using its folder path:

   ```bash
    docker compose -f docker/docker-compose.yml up --build
   ```

   ```bash
    docker-compose -f docker/docker-compose.yml up --build
   ```

2. Access the App

- curl http://localhost:8000/pokemon/pikachu
- curl http://localhost:8000/pokedex/1

3. Access monitoring dashboards:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (login: `admin`/`admin`)
