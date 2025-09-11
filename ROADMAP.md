## PRD.md (Product Requirements)


### 1. Problem / Goals
- **Problem:** Hard to capture real user pain/joy signals across forums.
- **Goal:** Self-hosted pipeline that listens, scores, surfaces, and emits suggestions.


### 2. Users
- **Analyst/Founder:** Prioritize roadmap with top findings.
- **Engineer/PM:** Stable API/feed of scored findings.


### 3. Scope (v1)
- Ingest: Reddit subs + HN.
- Persist: Postgres + Neo4j.
- Score: Heuristics (lexical + VADER + rules).
- Surface: `/v1/findings/market` + dashboard.
- Notify: NATS topics.


### 4. Functional Requirements
- Configurable sources.
- Deduplication + idempotency.
- Findings include: `source_id`, `artifact_id`, `score`, `polarity`, `rationale`, `excerpts`, `tags`.
- Graph edges (`MENTIONS`, `SIMILAR_TO`, `TAGGED_AS`).
- API with pagination + filters.


### 5. Non-functional
- Self-hostable (Docker Compose).
- CI: lint/type/test/build in <10m.
- Observability: health endpoints, logs.
- Backups: nightly Postgres, weekly Neo4j.
- Security: env-segregated secrets, least-priv DB, rotation policy.


### 6. Data Model
- **Tables:** sources, artifacts, notes, embeddings, events, suggestions.
- **Graph:** SOURCE→ARTIFACT (MENTIONS), ARTIFACT→ARTIFACT (SIMILAR_TO), ARTIFACT→TAG (TAGGED_AS).


### 7. APIs
- `GET /v1/findings/market`
- `POST /v1/ingest/manual`
- `GET /v1/artifacts/{id}`
- `GET /v1/graph/similar/{artifact_id}`


### 8. Scoring Logic
- Lexicon + VADER + rules → `score ∈ [0,1]`, `polarity`, `rationale`.


### 9. Ops & Rollout
- Environments: dev/staging/prod.
- CD: staging auto, prod manual.
- Backups + restore drills.


### 10. Acceptance Criteria
- Fresh clone boots + ingests sample + surfaces finding in <30 min.
- 200+ artifacts ingested with 90% dedup in 48h.
- CI blocking; smoke test passes.

---

### FILE: `ROADMAP.md`
```md
# Roadmap

## MVP (v0.1)
- Core & Full profiles; single internal network
- Next.js + Supabase auth (magic links)
- RAG on `/docs` with pgvector
- Observability (Grafana/Prometheus/Langfuse) + Low-Maintenance mode
- Marketplace (PR-curated), stars/likes
- Agents: seed hierarchy, write access with guardrails

## v0.2
- Air-gapped installer (pre-seeded images)
- SSO bridge: Authentik→Supabase mapping
- Caddy + Cloudflare Tunnel wizard
- Reranking & hybrid search (BM25 + vector)

## v0.3
- Agent eval harness in CI (RAG QA, tool use, summarization)
- SBOM & image signing (Syft/Cosign); Trivy gates
- Multi-network segmentation (DB/Secrets/Obs)
- On-site marketplace uploads + moderation queue
