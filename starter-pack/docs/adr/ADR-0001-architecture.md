
# ADR-0001: Reference Architecture Selection

## Decision
Adopt a modular, containerized stack: FastAPI (contracts), Postgres (OLTP), Neo4j (graph), NATS (events), n8n (automations).

## Context
We need a flexible platform to ingest public signals (Reddit, HN/YC), persist artifacts, derive insights, and route suggestions to humans and agents.

## Consequences
- Pros: clear boundaries, scalable, testable locally.
- Cons: more services to operate; requires secrets and backups.
