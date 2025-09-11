# BEST PRACTICES

> Location: `/docs/BEST_PRACTICES.md`  
> Purpose: speed up human + agent reasoning, reduce misalignment, and standardize how we work in Sushi Kitchen.

## 1) Master Bundles MUST Expand Full Content
- When generating concatenated master documents (Markdown/ZIP), **embed full file contents** (no placeholders).
- Separate each file with `--- FILE: path/filename ---`.
- Provide a **TOC** at the top linking to sections.

## 2) Deterministic-First Workflows
- Prefer deterministic n8n workflows for repeatable tasks.
- Use dynamic orchestration only when necessary; document the reason.
- Keep workflows in `/docs/workflows/` (SoC) and seed them into `/marketplace` when ready.

## 3) Single Source of Truth → Derived Artifacts
- PRD is the abstract source of truth; all other files derive from it (schemas, tasks, docs).
- Lock repo structure early to reduce agent confusion.

## 4) Schema Validation Everywhere
- Validate `/rolls` and `/platters` with JSON Schemas in `/schemas` before merging.
- CI enforces schema and compose validation.

## 5) Guardrails & Redaction
- Agents may not modify `docker-compose.yml`, `/schemas/*`, `.github/workflows/*` without human approval.
- Enable redaction in Langfuse by default; no secrets or PII in logs.

## 6) Inference Speed & Alignment (for Agents)
- Always consult `/docs` first for project conventions.
- Prefer exact file paths and explicit section references.
- Fail loudly with actionable errors when a guardrail blocks an operation.

## 7) Docs Placement
- Keep meta/governance/how-to-think docs in `/docs` (not repo root).
