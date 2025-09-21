# Architecture

- **Next.js (app router) + Tailwind UI + Supabase (auth/RLS)** on Vercel.
- **Docker Compose** with single internal network (MVP).
- **LLM**: Ollama (local) + LiteLLM (gateway to cloud, optional).
- **Workflows**: n8n (deterministic); dynamic agent orchestration allowed with guardrails.
- **RAG**: pgvector on Postgres; token-aware chunking; auto-sync `/docs` on merge; rerank in Phase 2.
- **Observability**: Prometheus→Grafana; Langfuse tracing (redaction on).
- **Security**: non-root containers, cap_drop, read-only FS where safe, secrets via `.env` (Infisical optional), encrypted backups.
