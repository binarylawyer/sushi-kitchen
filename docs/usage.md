
---

### FILE: `docs/usage.md`
```md
# Usage

## Choose a Profile
- **Lite** (`core`): postgres, n8n, ollama, litellm
- **Full**: + grafana, prometheus, langfuse, portainer, comfyui

## Try an Agent
- Import a sample workflow from `/workflows` (to be added).
- Ask the **Personal RAG Assistant** a question; it will retrieve from `/docs`.

## Rolls & Platters
- Drop a `.yml` into `/rolls` or `/platters`, then restart affected services.
- Validate with `pnpm -w validate:schema`.

## Marketplace
- Browse `/marketplace/catalog.yaml` for seed entries.
- Download artifacts and place in `/rolls`, `/platters`, or import into n8n.
