# Sushi Kitchen — Execution Tasks (MVP v0.1)

> Agent-friendly. Tasks are atomic, labeled, and reference PRD sections.  
> Tags: [infra], [web], [data], [agents], [obs], [security], [docs], [ci], [marketplace]

## 0. Repo Bootstrap
- [ ] T0.1 [infra] Create repo structure per README (apps/web, docs, schemas, prompts, marketplace, observability, workflows).
- [ ] T0.2 [ci] Add `.github/workflows/ci.yml` (lint, schema-validate, compose-validate, link-check, trivy).
- [ ] T0.3 [security] Add `LICENSE` (Apache-2.0), `SECURITY.md`, `CODEOWNERS`.
- [ ] T0.4 [infra] Add `.gitignore` + `.cursorignore` (block secrets, backups, logs, build dirs).

## 1. Compose & Profiles
- [ ] T1.1 [infra] Finalize `docker-compose.yml` (single internal network).
- [ ] T1.2 [infra] Define profiles: `core`, `observability`, `media`, `extras`.
- [ ] T1.3 [infra] GPU auto-detect (NVIDIA) + docs in `docs/install.md`.
- [ ] T1.4 [infra] Provide `docker-compose.override.yml` template for local dev.
- [ ] T1.5 [infra] (Phase 2) Caddy + Cloudflare Tunnel wizard.

## 2. Secrets & Security Baseline
- [ ] T2.1 [security] Provide `.env.example` with safe defaults + comments.
- [ ] T2.2 [security] Run containers non-root, `cap_drop=ALL` where feasible.
- [ ] T2.3 [security] Redaction toggles for Langfuse; agent guardrails enforcement.
- [ ] T2.4 [security] (Phase 2) Infisical bootstrap flow.

## 3. Data, RAG & Indexing
- [ ] T3.1 [data] Enable pgvector and create migrations.
- [ ] T3.2 [data] Implement token-aware chunking job.
- [ ] T3.3 [data] Provide retry strategy + idempotency for indexer.
- [ ] T3.4 [data] (Phase 2) Reranking plug-in interface.

## 4. Agents (Seed Hierarchy) & Tools
- [ ] T4.1 [agents] Implement Chef, Sous-Chef, Line-Cook, Quality-Check, Scribe roles.
- [ ] T4.2 [agents] Implement tool shims (DocSearch, Workflow.execute, QueryDB, WebFetch).
- [ ] T4.3 [security] Enforce guardrails (no compose/schemas edits).
- [ ] T4.4 [agents] Write audit trail `.logs/agent-audit.jsonl`.

## 5. Next.js Website (MVP)
- [ ] T5.1 [web] Scaffold Next.js + Tailwind UI + Supabase; add auth (magic links).
- [ ] T5.2 [web] Pages: Home, Docs, Install, Marketplace, Community, Privacy.
- [ ] T5.3 [web] Marketplace list/detail; star/like; gated submissions via PR (MVP).
- [ ] T5.4 [web] RLS policies for marketplace tables (public read, auth write).

## 6. Observability
- [ ] T6.1 [obs] Wire Prometheus; expose Docker metrics if safe.
- [ ] T6.2 [obs] Provision Grafana datasource + dashboards.
- [ ] T6.3 [obs] Add Langfuse instrumentation with redaction.
- [ ] T6.4 [obs] “Low-Maintenance” mode disables observability via `.env`.

## 7. Workflows (n8n)
- [ ] T7.1 [agents] Add `workflows/` exports (later pass) + README.
- [ ] T7.2 [docs] Document import steps in `/docs/usage.md`.

## 8. Marketplace Seeds
- [ ] T8.1 [marketplace] Seed `catalog.yaml` with 3 platters.
- [ ] T8.2 [marketplace] Add contribution guidelines in `CONTRIBUTING.md`.

## 9. CI/CD Hardening
- [ ] T9.1 [ci] Add markdownlint, Vale, spellcheck configs.
- [ ] T9.2 [ci] JSON Schema validation for `/schemas`.
- [ ] T9.3 [ci] Lighthouse CI on Vercel Preview.
- [ ] T9.4 [ci] Nightly compose boot test (no-op if `ENABLE_OBSERVABILITY=false`).

## 10. Docs
- [ ] T10.1 [docs] Complete install/usage/architecture/security/observability/agents/developers/faq.
- [ ] T10.2 [docs] Mermaid diagrams under `docs/_diagrams` (optional).
- [ ] T10.3 [docs] Versioned URLs (tag-based) – placeholder for v0.2.
