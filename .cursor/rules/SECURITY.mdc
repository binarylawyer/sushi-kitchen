
# SECURITY.md

This doc outlines minimum security baselines for ULOS.

## Secrets
- Never commit real secrets. Use `.env` locally and a secrets manager in prod (1Password, Doppler, Vault, AWS/GCP).
- Rotate high-value creds every 90 days. Use distinct DB users per service with least privilege.

## Network & Data
- Default-deny inbound; expose only necessary ports.
- Enforce TLS in production; terminate at the edge or at the ingress.
- Backups: daily Postgres and weekly Neo4j with 14–30 day retention. Test restores quarterly.

## Application
- Add auth (API keys or OAuth) before any external exposure.
- Rate limit write endpoints. Validate all inputs with Pydantic.
- Add allowlists for n8n webhooks; prefer NATS for internal calls.

## Compliance & Logging
- Centralize logs. Avoid writing PII to logs. Document retention policy.
- Keep an up-to-date Data Map and threat model. Run dependency scans weekly.

# Security Policy

## Philosophy
Local-first and privacy-focused. We minimize egress, run services with least privilege, and provide redaction by default.

## Supported Versions
- Actively supported: latest `main` and the most recent tagged release (v0.x).
- Security fixes may be backported at our discretion.

## Reporting a Vulnerability
- Email: **security@sushi.dev**
- Or open a **GitHub Security Advisory** (private).
- Include: affected version/commit, environment, PoC steps, expected/actual behavior, and impact.

We acknowledge reports within **72 hours**, provide an initial assessment within **5 business days**, and share a remediation ETA.

## Scope
- Repository code, Docker Compose services, Next.js web app.
- Marketplace items hosted in this repo.

Out of scope: 3rd-party dependencies’ vulnerabilities (report upstream), user-customized deployments.

## Handling Sensitive Data
- Do not include secrets in issues or PRs.
- Sanitized logs only; Langfuse redaction enabled by default.
- Use encrypted backups and BYOK passphrases.

## Hardening Baseline
- Non-root containers; `cap_drop=ALL` when feasible.
- Read-only filesystems for stateless services.
- Single private Docker network (MVP), segmentation later.
- Strict agent guardrails: no edits to `docker-compose.yml`, `/schemas/*`, `.github/workflows/*` without human approval.
