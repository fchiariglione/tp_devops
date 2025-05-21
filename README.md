# Pokedex API - FastAPI Microservice

A FastAPI-based RESTful API that provides Pokedex information with metrics, monitoring, and complete CI pipeline.

## Features

- RESTful API for Pokemon data access
- Prometheus metrics collection
- Grafana dashboards for monitoring
- Loki for log aggregation
- Multi-stage Docker builds
- Comprehensive CI/CD pipeline with GitHub Actions
- Multi-environment deployment (dev, staging, production)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pokemon/{name}` | GET | Get Pokemon by name |
| `/pokedex/{id}` | GET | Get Pokemon by Pokedex number |
| `/pokemon` | POST | Create a new Pokemon |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Swagger UI documentation |

## Tech Stack

- **Backend:** FastAPI, Python 3.13
- **Containerization:** Docker, Docker Compose
- **Monitoring:** Prometheus, Grafana, Loki
- **CI/CD:** GitHub Actions
- **Testing:** Pytest

## Prerequisites

- Docker & Docker Compose
- Python 3.13+ (for local development)

## Local Development

### With Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/user/pokedexapi.git
   cd pokedexapi
   ```

2. **Start the development environment:**
   ```bash
   docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000/docs
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (login: admin/admin)

### Without Docker

1. **Clone the repository:**
   ```bash
   git clone https://github.com/user/pokedexapi.git
   cd pokedexapi
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API:**
   - API: http://localhost:8000/docs

## Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Deployment

### Staging Environment

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.staging.yml up -d
```

### Production Environment

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
```

## CI/CD Pipeline

The project uses GitHub Actions for CI/CD:

1. **On every push:**
   - Run tests
   - Perform linting
   - Conduct security scanning

2. **On push to dev, staging, or main:**
   - Build multi-architecture Docker images
   - Push to Docker Hub
   - Deploy to appropriate environment (for staging and main branches)

## Monitoring & Observability

### Metrics

Access Prometheus metrics at: http://localhost:9090

### Dashboards

Grafana dashboards are available at: http://localhost:3000
- Default login: admin/admin

Pre-configured dashboards:
- Pokemon API Overview: Request rates, latencies, and error rates
- System Metrics: CPU, memory, and network usage
- Logs: Application logs aggregated by Loki

### Logs

Logs are collected by Promtail and stored in Loki, viewable through Grafana.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
