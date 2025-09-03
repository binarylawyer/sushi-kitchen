🍣 Sushi Kitchen Menu (v0.1 “Omakase”)

A curated set of rolls (profiles). Each roll lists its “ingredients” (apps), defaults, and what hardware it targets. You can enable/disable rolls from the sushi-start.sh menu or with Compose profiles.

🍙 Hosomaki — Core Foundation (Default ON)

What it is: the control plane + essential data layer.
Use it for: building automations and apps; everything else layers on top.

Ingredients

Caddy (reverse proxy)

n8n (automation/orchestration)

LiteLLM (LLM router: local-first, cloud fallback)

Postgres + pgvector (relational + embeddings)

Qdrant (default vector DB)

Redis (cache/queues)

Ollama (local LLMs; 7B/13B quant)

MinIO (local S3-compatible datastore)

Homepage (launchpad)

Defaults

✅ Enabled for all presets (Windows 16 GB, Mac mini 24 GB, Monster)

Qdrant ON; Neo4j OFF by default (see Futomaki)

🍣 Futomaki — Knowledge & RAG

What it is: retrieval pipelines and graph knowledge.
Use it for: RAG apps, semantic search, graph exploration.

Ingredients

Neo4j (graph DB) — toggle ON as needed

(À la carte) Weaviate, Chroma (extra vectors, off by default)

(Optional) Infinity (high-perf embedding server)

Defaults

🟡 Off by default on laptops; toggle Neo4j when you need graph features.

Only one vector DB hot at a time (Qdrant default).

🍤 Temaki — Voice & Interaction

What it is: speech in/out.
Use it for: transcription, TTS, callflows.

Ingredients

Whisper (small/medium by default)
- Whisper (GPU) – see `compose/docker-compose.whisper.yml`


Piper (TTS)

Defaults

✅ On for all presets (small/medium models)

Whisper large-v3 runs in Cloud or Monster preset.

🎨 Uramaki — Imaging

What it is: image generation pipelines.
Use it for: SD 1.5 locally, SDXL in the cloud.

Ingredients

ComfyUI (node graph)
- ComfyUI (GPU) – see `compose/docker-compose.comfyui.yml`


(Sidecar) rclone → pushes outputs to MinIO/S3

Defaults

🟡 Off by default on laptops.

SD 1.5 acceptable locally (run it alone).

SDXL is Cloud/Monster only.

🧪 Chirashi — Data Science

What it is: notebooks + light data wrangling.
Use it for: prototyping, EDA, small finetunes.

Ingredients

JupyterLab (persistent volume mapped to /home/jovyan/work)

(Docs/Examples) S3 helpers, dataset templates

Defaults

✅ On for all presets (lightweight)

Dask available À la carte (off by default).

🥚 Tamago — Dev Tools (Optional)

What it is: web IDEs and helpers.
Use it for: browser-based dev flows.

Ingredients

VS Code Server (optional)

Defaults

🟡 Off by default; enable if you want a web IDE.

🐉 Dragon Roll — Observability (Light by Default)

What it is: metrics + tracing (+ optional logs).
Use it for: seeing what’s going on, quickly.

Ingredients

Prometheus (24 h retention by default)

Grafana (dashboards)

cAdvisor + Node Exporter (resource metrics)

Langfuse (LLM traces; toggle on when tracing)

(Enterprise) Loki + Promtail (central logs, off by default)

Defaults

✅ Light metrics on (Prom 24 h + Grafana + exporters)

🟡 Langfuse optional; 🟡 Loki/Promtail off on laptops.

🔐 Hanko — Identity (Enterprise Optional)

What it is: SSO and access control.
Use it for: multi-user security.

Ingredients

Authentik (OIDC/SAML)

Caddy forward-auth (protect UIs)

Defaults

🟡 Off by default; enable in “enterprise” install.

🧂 Shio — Secrets (Enterprise Optional)

What it is: centralized secret management.
Use it for: eliminating .env sprawl, rotation.

Ingredients

Infisical CE (or Vault OSS)

Defaults

🟡 Off by default; enable in “enterprise” install.

🥒 Tsukemono — Backups (Optional)

What it is: disaster recovery for data/services.
Use it for: automated encrypted backups.

Ingredients

Borgmatic (volumes)

pgBackRest / wal-g (Postgres)

(Scripts) neo4j-admin backup cron

Defaults

🟡 Off by default; provide ready jobs and docs.

⚡ Gunkanmaki — Pro Inference (Hybrid / Cloud)

What it is: high-throughput LLM serving.
Use it for: low-latency, high-concurrency APIs.

Ingredients

vLLM (OpenAI-compatible server)

LiteLLM routing (local → vLLM cloud fallback)

Defaults

🟡 Local vLLM off on laptops.

✅ Cloud compose included (GPU VM).

🍽️ À la carte Dishes (Advanced, Off by Default)

Weaviate (vector DB) — alternative to Qdrant

Chroma (vector DB) — rapid prototypes, notebook-native

Memgraph, ArangoDB — deferred; not in v0.1 binaries

Loki + Promtail — enable as part of “enterprise” ops

Dask — for larger data jobs in Jupyter

Infinity — dedicated embeddings server

Automatic1111 — deferred; consider recipe-only later

✅ Final App Selection — v0.1 First Release

In (Default or One-Click Optional)

Default ON

Caddy, n8n, LiteLLM, Postgres+pgvector, Qdrant, Redis, Ollama, MinIO, Homepage

Prometheus (24 h), Grafana, cAdvisor, Node Exporter

JupyterLab

Optional (clearly surfaced in menu)

Neo4j (toggle)

Langfuse (LLM tracing)

Whisper small/medium + Piper

ComfyUI (SD 1.5 local; SDXL via cloud)

VS Code Server

Loki/Promtail (enterprise)

Authentik (enterprise)

Infisical (enterprise)

Borgmatic + pgBackRest (backups)

vLLM (cloud compose by default; local on Monster)

Included as À la carte (Off by default)

Weaviate, Chroma (vector alternatives)

Dask, Infinity (advanced DS/RAG utilities)

🧹 Moved Out / Deferred (to reduce sprawl & confusion)

Removed from defaults; available À la carte or later

Weaviate & Chroma: Not in presets. Only via À la carte selector.
Reason: avoid “vector sprawl”; Qdrant is default, stable and light.

Neo4j: Off by default, toggle when needed.
Reason: save ~1–2 GB idle; keep graph optional.

Loki/Promtail: enterprise optional.
Reason: log volume + admin overhead on small machines.

vLLM (local): off by default (laptops); ship cloud compose as primary path.
Reason: throughput belongs on a GPU VM for most users.

Automatic1111: deferred (ComfyUI already covers pipelines; keep docs/recipe for UI preference).

Memgraph, ArangoDB: deferred to a later release.
Reason: minimize cognitive load; most needs met by Neo4j.

Ray / distributed training: deferred / enterprise later.
Reason: 95% of users won’t have multi-GPU clusters; fit this into a dedicated “Washoku” later if demand shows up.

🧭 How this maps to the repo (quick index)

compose/docker-compose.base.yml → Hosomaki

compose/docker-compose.rag.yml → Futomaki (Qdrant default, Neo4j toggle; À la carte: Weaviate/Chroma)

compose/docker-compose.media.yml → Uramaki (ComfyUI + rclone), Temaki (Whisper svc)

compose/docker-compose.devtools.yml → Chirashi (Jupyter), Tamago (VS Code Server)

compose/docker-compose.obs.yml → Dragon Roll (Prom/Grafana/exporters; Loki/Promtail opt-in)

compose/docker-compose.security.yml → Hanko (Authentik + forward-auth)

compose/docker-compose.secrets.yml → Shio (Infisical)

compose/docker-compose.backups.yml → Tsukemono (Borgmatic + pgBackRest)

compose/docker-compose.cloud.yml → Gunkanmaki (LiteLLM -> vLLM fallback, Whisper large/ComfyUI SDXL endpoints)

🧠 Rationale (why this v0.1 cut will feel great)

Opinionated, not overwhelming: one vector (Qdrant) + optional graph (Neo4j) → less RAM/ports, less choice paralysis.

Local-first dev loop: n8n + Jupyter + Ollama + Qdrant work beautifully on laptops/Mac minis.

Hybrid by design: heavy lifts (vLLM, SDXL, Whisper large) ship as cloud compose out of the box.

SRE when you want it: enterprise preset adds SSO, secrets, logs — not forced on hobbyists.

Docs match the menu: each roll’s purpose is plain English; users understand what they’re enabling.

If you’d like, I can generate the actual docs/menu.md file and a “Menu” section in README.md with the exact emojis and toggles wired to the sushi-start.sh options you already have — so it’s fully consistent with the repo scaffolding we drafted.