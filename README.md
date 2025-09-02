
# ULOS Consciousness Engine — Starter Pack

This repo scaffolds the core services and workflows for the ULOS/Sushi Kitchen project.

## Services
- **API (FastAPI)**: contracts and endpoints for ingest, artifacts, notes, embeddings, and findings.
- **Postgres**: primary store for artifacts and notes.
- **Neo4j**: knowledge graph (sources, artifacts, tags, relationships).
- **NATS**: async messaging and suggestions.
- **n8n**: listener workflows for Reddit and Hacker News (YC).

## Quick Start
1. `cp .env.example .env` and edit values.
2. `docker compose up -d`
3. `make db-migrate`
4. Import `n8n/workflows/*.json` into n8n and test.

## Paths
- `app/` — FastAPI application
- `migrations/` — Postgres DDL
- `neo4j/` — graph constraints / setup
- `n8n/workflows/` — listener automations
- `docs/` — ADRs and design notes
