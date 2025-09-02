
SHELL := /bin/bash

.PHONY: up down logs rebuild db-migrate fmt lint

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

rebuild:
	docker compose up -d --build api

db-migrate:
	psql postgresql://$${POSTGRES_USER}:$${POSTGRES_PASSWORD}@localhost:$${POSTGRES_PORT}/$${POSTGRES_DB} -f migrations/0001_init.sql

fmt:
	@echo "Add your formatter (ruff/black) here"

lint:
	@echo "Add your linter (ruff/mypy) here"
