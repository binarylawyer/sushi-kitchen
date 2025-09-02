
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
