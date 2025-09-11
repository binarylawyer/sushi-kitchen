# Agents

## Seed Hierarchy (MVP)
- **Chef (Coordinator)**: plans tasks; decides deterministic (n8n) vs dynamic.
- **Sous-Chef (Docs/RAG)**: retrieves from `/docs` (pgvector); answers + citations.
- **Line-Cook (WorkflowExec)**: executes n8n flows; returns artifacts.
- **Quality-Check (Safety)**: enforces guardrails (no compose edits, no disallowed tools).
- **Scribe (Committer)**: writes files; opens PRs; attaches audit notes.

## Tools (allowlist)
- `DocSearch(query)` → RAG snippets
- `Workflow.execute(name, params)` → runs n8n
- `QueryDB(sql)` → safe, parameterized
- `WebFetch(query)` → via proxy (SearxNG) [optional]
- (Phase 2) `Secrets.get(name)` via Infisical proxy

## Guardrails
- Never modify: `docker-compose.yml`, `/schemas/*`, `.github/workflows/*` without human OK.
- Respect `.cursorignore` (no reading/writing ignored paths).
- Redact secrets before logging.

## Audit
- All agent writes → `.logs/agent-audit.jsonl` (timestamp, file path, diff hash, reason)
- PR comments include summary of changes & links to logs.
