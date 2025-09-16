# Personas & Journeys — Sushi Kitchen

## Personas

### Indie Builder (Aki)
- Goals: ship an internal tool; small budget; prefers local.
- Frictions: GPU setup, secrets, routing.
- KPIs: time to first working app, docs clarity.

### Team Dev Lead (Sam)
- Goals: reliable stack for 5–20 engineers; SSO; audit.
- Frictions: observability, RBAC, backups.
- KPIs: onboarding time, MTTR, policy compliance.

### Data tinkerer (Rae)
- Goals: notebooks + viz + model tracking.
- Frictions: storage sprawl, reproducibility.
- KPIs: experiment velocity, shareable dashboards.

## Journeys

### J1 — Stand up the kitchen (90 minutes)
1. Clone repo → `docker compose up -d`
2. Visit `/auth` (Authentik), set admin
3. Configure Infisical, add provider keys
4. Pull first model in Ollama; test via LiteLLM `/v1` route
5. Create first workflow in n8n

### J2 — RAG workspace with citations
1. Launch AnythingLLM → connect Qdrant
2. Upload PDFs → index → test chat
3. Add Langfuse keys → verify traces

### J3 — Render a product video
1. Create Remotion project (template)
2. Add VO track (OpenVoice) + music
3. Render via API → MinIO → share link

### J4 — Observe & debug
1. Grafana dashboards (CPU/GPU, LLM latency)
2. Langfuse spans for prompts/tool calls
3. Loki logs for noisy services (optional)
