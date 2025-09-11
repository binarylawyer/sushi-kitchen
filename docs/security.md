# Security & Privacy

- **Data sovereignty**: local-first, no telemetry.
- **Network**: single private bridge network; no public ports unless explicitly mapped.
- **Containers**: non-root, minimal capabilities, read-only FS where possible.
- **Secrets**: `.env` (do not commit); Infisical optional (Phase 2).
- **Backups**: encrypted (BYOK passphrase) recommended; store keys separate from backup blobs.
- **Logging & Tracing**: Langfuse with redaction; PII/secret masking.
- **Agent Guardrails**:
  - Cannot directly modify `docker-compose.yml` or `/schemas` without human approval.
  - Restricted tool allowlist; no raw `curl`/shell net without proxy.
  - Folder sandbox: `.cursorignore` excludes `/db_backups`, `/.logs`, `.env*`, secrets.
