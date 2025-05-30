# Makefile for Pokedex API

# Variables
DOCKER_COMPOSE_DEV=docker/docker-compose.dev.yml
DOCKER_COMPOSE_PROD=docker/docker-compose.prod.yml
DOCKER_COMPOSE_STAGING=docker/docker-compose.staging.yml
DOCKER_COMPOSE_BASE=docker/docker-compose.yml

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build-dev        Build Docker images for development"
	@echo "  up-dev           Start dev environment with Docker Compose"
	@echo "  down-dev         Stop dev environment"
	@echo "  build-prod       Build Docker images for production"
	@echo "  up-prod          Start production environment with Docker Compose"
	@echo "  down-prod        Stop production environment"
	@echo "  build-staging    Build Docker images for staging"
	@echo "  up-staging       Start staging environment with Docker Compose"
	@echo "  down-staging     Stop staging environment"
	@echo "  test             Run tests with pytest (local)"
	@echo "  lint             Run linting with flake8 (local)"
	@echo "  clean            Remove Python cache and Docker images"
	@echo "  run-local        Run the app locally with uvicorn"

# Docker Compose targets
build-dev:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_DEV) build

up-dev:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_DEV) up --build "api"

down-dev:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_DEV) down

build-prod:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_PROD) build

up-prod:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_PROD) up -d --build "api"

down-prod:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_PROD) down

build-staging:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_STAGING) build

up-staging:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_STAGING) up -d --build 

down-staging:
	docker compose -f $(DOCKER_COMPOSE_BASE) -f $(DOCKER_COMPOSE_STAGING) down

# Local development targets
test:
	pytest

lint:
	flake8 app

run-local:
	uvicorn app.main:app --reload

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache app/__pycache__
	docker system prune -f 