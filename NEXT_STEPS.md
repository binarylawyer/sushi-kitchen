## NEXT_STEPS.md (Execution Checklist)


### Phase 0 — Repo Hardening (Today)
- [ ] Create protected branches (`main`, `dev`) and require PRs + status checks.
- [ ] Add CODEOWNERS and PR template.
- [ ] Enable branch rules, secrets scanning, Dependabot, and required reviews.
- [ ] Add CI jobs (lint, type-check, test, build) via GitHub Actions.


### Phase 1 — Environment + Core Services
- [ ] Copy `.env.example` → `.env` and fill in secrets.
- [ ] `docker compose up -d` to boot: api, postgres, neo4j, nats, n8n.
- [ ] Run `make db-migrate` to apply SQL migrations.
- [ ] Open Neo4j Browser and run `neo4j/init.cql` (or use APOC auto-run).


### Phase 2 — API Contracts + Schemas
- [ ] Flesh out Pydantic models and OpenAPI tags in `app/`.
- [ ] Lock core entities: `Source`, `Ingest`, `Artifact`, `Note`, `Tag`, `Embedding`, `Event`, `Suggestion`.
- [ ] Add versioned API routes (`/v1/*`) with request/response examples.


### Phase 3 — Listening Pack (n8n)
- [ ] Import `n8n/workflows/reddit_listen.json` and `hn_yc_listen.json`.
- [ ] Configure credentials and test sample runs.
- [ ] Persist outputs to Postgres (artifacts + sources).
- [ ] Push graph edges to Neo4j (`MENTIONS`, `SIMILAR_TO`).


### Phase 4 — Scoring & Surfacing
- [ ] Implement dissatisfaction/satisfaction heuristics (lexical cues, VADER, rule-based).
- [ ] Add a simple `/v1/findings/market` endpoint and dashboard view in n8n or a minimal Next.js frontend.
- [ ] Wire NATS topics for async suggestions (`market.findings.*`).


### Phase 5 — Security & Ops
- [ ] Complete SECURITY.md items (Vault, least privilege, secret rotation policy).
- [ ] Add monitoring (health checks, basic metrics), and backups for Postgres/Neo4j.
- [ ] Decide on deployment target (Fly.io, Railway, Render, k8s).
- [ ] Add a GitHub Actions CD job.


#### Quick Commands
- Start stack: `docker compose up -d`
- Stop stack: `docker compose down -v`
- Migrate DB: `make db-migrate`
- Tail logs: `docker compose logs -f api`
- Rebuild API: `docker compose up -d --build api`