# TP DevOps FastAPI Pokedex

## Requirements

- Docker & Docker Compose
- kubectl & kind (or minikube)

## Swagger

- http://localhost:8000/docs

## Local Docker Development

1. From the project root, run Docker Compose using its folder path:

   **Dev**
   ```bash
    docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up --build
   ```

   **Staging**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d
   ```

   **Prod**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

2. Access the App
- curl http://localhost:8000/pokemon/pikachu
- curl http://localhost:8000/pokedex/1

3. Access monitoring dashboards:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (login: `admin`/`admin`)
