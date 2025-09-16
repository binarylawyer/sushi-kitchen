
---

## `.cursor/rules/project_overview.md`
```md
# Project Overview — Sushi Kitchen

## Elevator pitch
A self-hosted, professional-grade AI kitchen: compose LLM, RAG, vision, voice, and video services with a click; ship apps fast with secure, observable defaults.

## Goals
- Single source of truth for services and routes
- Safe-by-default edge exposure (auth, rate-limits)
- Developer joy: batteries-included workflows and tools

## Non-goals
- Competing with full cloud platforms
- Managing user PII beyond identity/secrets

## Architecture (text sketch)
- **Edge**: Caddy/Cloudflare → Authentik → service routes
- **Core**: Hosomaki (n8n, LiteLLM, Ollama/vLLM)
- **Storage**: Futomaki (Supabase/Postgres, Qdrant, MinIO, Redis)
- **Media**: Uramaki (images), Ramen (video)
- **Observability**: Inari (Prometheus/Grafana/Langfuse)
- **Security**: Gunkanmaki (Authentik, Infisical)
- **Dev**: Temaki (VS Code Server, Flowise, Dify)
- **Data science**: Chirashi (Jupyter, MLflow, Metabase)

## Key workflows
- Chat/RAG → AnythingLLM ↔ Qdrant ↔ LiteLLM
- Image gen → ComfyUI → rclone → MinIO
- Video render → Remotion → FFmpeg → MinIO
- Telemetry → OTel Collector → Prometheus/Grafana; LLM traces → Langfuse

## Deployment
- Docker Compose default; K8s overlays optional
- GPU optional (Ollama/vLLM/ComfyUI/FFmpeg filters)

## Roadmap (short)
- v0: SSOT, menu site, stable Compose
- v1: CI lint + generators, basic RBAC, backups flow
- v1.1: Enterprise “Kaiseki” presets, K8s overlay
