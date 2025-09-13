---
# ============================================================
# 🍣 Sushi Kitchen — Menu Manifest (Human-facing catalog only)
# Version: 2.3  (previous saved as 2.2 per your note)
# Schema: front matter for website/homepage rendering.
# IMPORTANT:
#  - Keep ONLY presentational fields here (ids, names, notes, badges).
#  - Move operational fields (docker_image, versions, ports, env, deps)
#    to `docs/manifest/contracts.yml`.
#  - Combos live in `docs/manifest/combos.yml`
#  - Platters live in `docs/manifest/platters.yml`
#  - Badge definitions (labels/tooltips) live in `docs/manifest/badges.yml`
#    with SVGs in `assets/badges/`.
# This separation stops drift and makes CI automation easy.
# ============================================================

title: "🍣 Sushi Kitchen Menu Manifest"
version: "2.3"
manifest_schema_version: "1.1"   # bumped because we split concerns formally
last_updated: 2025-09-12
legend: "✅ recommended · ⚖️ optional"

# Optional, non-operational repo-wide metadata that UIs may show.
# (Safe to keep here because it’s not brittle like image tags.)
deployment_targets:
  - docker-compose
  - kubernetes
  - docker-swarm

privacy_profiles_supported:
  - chirashi
  - temaki
  - inari

# NOTE on badges:
# Use badge KEYS only (e.g., popular, optional, gpu, gpu-optional, enterprise, heavy, experimental, k8s, future, ci).
# The dictionary and icons are defined in:
#   docs/manifest/badges.yml  +  assets/badges/*.svg

# NOTE on styles:
# `color_theme` is fine here (purely UI). Any `port_range` previously used
# is now assigned per-roll in contracts.yml so there are no collisions.
styles:

  # ========================
  # 1) Hosomaki — Foundation
  # ========================
  - name: Hosomaki
    description: "Thin rolls — the core foundation."
    color_theme: "#2C3E50"
    rolls:
      - id: hosomaki.ollama
        name: "Ollama"
        status: recommended
        badges: [popular, gpu-optional]
        notes: "Local LLM engine with a huge community."
      - id: hosomaki.litellm
        name: "LiteLLM"
        status: recommended
        badges: [popular]
        notes: "Universal API gateway for local + cloud LLMs."
      - id: hosomaki.n8n
        name: "n8n"
        status: recommended
        badges: [popular]
        notes: "Workflow automation/orchestration brain."
      - id: hosomaki.supabase
        name: "Supabase"
        status: recommended
        badges: [popular]
        notes: "Postgres + pgvector backend with auth & realtime."
      - id: hosomaki.redis
        name: "Redis"
        status: recommended
        notes: "Cache & queue; speeds async tasks."
      - id: hosomaki.caddy
        name: "Caddy"
        status: recommended
        notes: "Modern reverse proxy with automatic HTTPS."
      - id: hosomaki.portainer
        name: "Portainer"
        status: optional
        badges: [optional]
        notes: "Optional Docker GUI for homelab visibility."

  # ===========================================
  # 2) Futomaki — Knowledge & RAG (DBs/Graphs)
  # ===========================================
  - name: Futomaki
    description: "Fat rolls — knowledge stores, RAG, and graphs."
    color_theme: "#27AE60"
    rolls:
      - id: futomaki.qdrant
        name: "Qdrant"
        status: recommended
        badges: [popular]
        notes: "High-performance vector database for RAG."
      - id: futomaki.chroma
        name: "Chroma"
        status: recommended
        notes: "Simple prototyping vector store."
      - id: futomaki.weaviate
        name: "Weaviate"
        status: optional
        badges: [optional, enterprise]
        notes: "GraphQL-native vector DB; enterprise-leaning alternative."
      - id: futomaki.neo4j
        name: "Neo4j"
        status: recommended
        notes: "Graph database powerhouse — great for GraphRAG."
      - id: futomaki.memgraph
        name: "Memgraph"
        status: optional
        badges: [optional]
        notes: "In-memory graph DB; niche alternative."
      - id: futomaki.arangodb
        name: "ArangoDB"
        status: optional
        badges: [optional, heavy]
        notes: "Multi-model DB (graph+doc+KV); heavier footprint."
      - id: futomaki.anythingllm
        name: "AnythingLLM"
        status: recommended
        badges: [popular]
        notes: "Turnkey RAG UI with strong community."
      - id: futomaki.infinity
        name: "Infinity (Embeddings)"
        status: recommended
        notes: "Fast embedding server for sentence transformers."
      - id: futomaki.flowise
        name: "Flowise"
        status: optional
        badges: [optional]
        notes: "Visual LangChain builder; no-code agent graphs."
      - id: futomaki.dify
        name: "Dify"
        status: optional
        badges: [optional]
        notes: "LangSmith-style orchestration; OSS flavor."

  # ==========================================
  # 3) Temaki — Voice & Interaction (ASR/TTS)
  # ==========================================
  - name: Temaki
    description: "Hand rolls — voice, interaction, and conversation."
    color_theme: "#E74C3C"
    rolls:
      - id: temaki.whisper
        name: "Whisper"
        status: recommended
        badges: [gpu-optional]
        notes: "ASR with near human-level accuracy."
      - id: temaki.piper
        name: "Piper"
        status: recommended
        notes: "Lightweight text-to-speech."
      - id: temaki.openvoice
        name: "OpenVoice"
        status: optional
        badges: [optional, experimental]
        notes: "Voice cloning; early-stage expectations."
      - id: temaki.openui
        name: "OpenUI"
        status: optional
        badges: [optional, experimental]
        notes: "Experimental UI generator for conversational apps."
      - id: temaki.open-webui
        name: "Open WebUI"
        status: recommended
        badges: [popular]
        notes: "Popular Ollama/LLM chat UI."
      - id: temaki.adorable-clone
        name: "Adorable.dev (clone)"
        status: optional
        badges: [optional, experimental]
        notes: "In-house playful UI alternative."

  # ================================================
  # 4) Uramaki — Visual / Creative (Image/Video/IO)
  # ================================================
  - name: Uramaki
    description: "Inside-out rolls — creative, visual, and media."
    color_theme: "#9B59B6"
    rolls:
      - id: uramaki.comfyui
        name: "ComfyUI"
        status: recommended
        badges: [popular, gpu]
        notes: "Node-based Stable Diffusion pipelines; GPU recommended."
      - id: uramaki.ffmpeg
        name: "FFmpeg"
        status: recommended
        notes: "Swiss-army knife for audio/video processing."
      - id: uramaki.remotion
        name: "Remotion"
        status: optional
        badges: [optional]
        notes: "Programmatic video generation."
      - id: uramaki.scanned
        name: "Scanned"
        status: optional
        badges: [optional, experimental]
        notes: "Video analysis utilities; early stage."
      - id: uramaki.rclone
        name: "rclone"
        status: recommended
        notes: "Sync to S3/MinIO/GDrive; storage glue."
      - id: uramaki.imagemagick
        name: "ImageMagick"
        status: recommended
        notes: "Classic image manipulation toolkit."

  # ============================================
  # 5) Dragon Roll — Observability & Governance
  # ============================================
  - name: Dragon Roll
    description: "Oversight — observability, logs, tracing, quality."
    color_theme: "#F39C12"
    rolls:
      - id: dragon.prometheus
        name: "Prometheus"
        status: recommended
        notes: "Metrics collection standard."
      - id: dragon.grafana
        name: "Grafana"
        status: recommended
        notes: "Dashboards and observability hub."
      - id: dragon.cadvisor
        name: "cAdvisor"
        status: recommended
        notes: "Container-level resource metrics."
      - id: dragon.langfuse
        name: "Langfuse"
        status: recommended
        notes: "LLM tracing/analytics."
      - id: dragon.otel-collector
        name: "OpenTelemetry Collector"
        status: recommended
        notes: "Unified telemetry ingestion."
      - id: dragon.loki
        name: "Loki"
        status: optional
        badges: [optional]
        notes: "Log aggregation (Grafana stack)."
      - id: dragon.promtail
        name: "Promtail"
        status: optional
        badges: [optional]
        notes: "Log shipper; pairs with Loki."
      - id: dragon.sonarqube
        name: "SonarQube"
        status: optional
        badges: [optional, ci]
        notes: "Code quality/vulnerability scanning (dev/CI focus)."
      - id: dragon.istio
        name: "Istio"
        status: optional
        badges: [optional, enterprise, k8s, future]
        notes: "Service mesh; K8s/enterprise roadmap."
      - id: dragon.traefik
        name: "Traefik"
        status: optional
        badges: [optional, enterprise, future]
        notes: "Alt reverse proxy; enterprise futures."

  # ==================================
  # 6) Tamago — Developer Tooling
  # ==================================
  - name: Tamago
    description: "Egg — developer tools, simple yet skilled."
    color_theme: "#1ABC9C"
    rolls:
      - id: tamago.vscode-server
        name: "VS Code Server"
        status: recommended
        notes: "Web IDE in the browser."
      - id: tamago.jupyterlab
        name: "JupyterLab"
        status: recommended
        notes: "Notebook environment for DS/AI."
      - id: tamago.panel
        name: "Panel"
        status: optional
        badges: [optional]
        notes: "Lightweight dashboarding for data apps."
      - id: tamago.dask
        name: "Dask"
        status: optional
        badges: [optional, heavy]
        notes: "Parallel computing; heavier footprint."
      - id: tamago.docusaurus
        name: "Docusaurus"
        status: recommended
        notes: "Docs site generator."
      - id: tamago.duckdb
        name: "DuckDB"
        status: optional
        badges: [optional, popular]
        notes: "Fast analytics DB — ‘SQLite for OLAP’."
      - id: tamago.sqlite
        name: "SQLite"
        status: optional
        badges: [optional]
        notes: "Ubiquitous embedded relational DB."

  # ==========================================
  # 7) Spider Roll — MLOps & Experimentation
  # ==========================================
  - name: Spider Roll
    description: "Intricate — MLOps, experiments, orchestration."
    color_theme: "#34495E"
    rolls:
      - id: spider.mlflow
        name: "MLflow"
        status: recommended
        notes: "Track experiments, metrics, and artifacts."
      - id: spider.ray
        name: "Ray"
        status: optional
        badges: [optional, heavy]
        notes: "Distributed training/serving; heavy but powerful."
      - id: spider.bentoml
        name: "BentoML"
        status: optional
        badges: [optional]
        notes: "Model serving/deployment toolkit."
      - id: spider.kubeflow
        name: "Kubeflow"
        status: optional
        badges: [optional, enterprise, k8s, future, heavy]
        notes: "End-to-end ML pipelines; enterprise/K8s roadmap."
      - id: spider.temporal
        name: "Temporal"
        status: optional
        badges: [optional]
        notes: "Durable workflow orchestration."

  # =========================================
  # 8) Shoyu — Data Lifecycle & Management
  # =========================================
  - name: Shoyu
    description: "Soy sauce — storage, backup, data lifecycle."
    color_theme: "#8B4513"
    rolls:
      - id: shoyu.minio
        name: "MinIO"
        status: recommended
        notes: "S3-compatible object storage."
      - id: shoyu.restic
        name: "Restic"
        status: recommended
        notes: "Encrypted, deduplicated backups."
      - id: shoyu.duplicati
        name: "Duplicati"
        status: optional
        badges: [optional]
        notes: "GUI backup; simpler flows."
      - id: shoyu.pgadmin
        name: "pgAdmin"
        status: recommended
        notes: "Web UI for Postgres."
      - id: shoyu.redisinsight
        name: "RedisInsight"
        status: optional
        badges: [optional]
        notes: "GUI for Redis monitoring/queries."
      - id: shoyu.borgbackup
        name: "BorgBackup"
        status: optional
        badges: [optional]
        notes: "Efficient dedup backups."
      - id: shoyu.pgbackrest
        name: "pgBackRest"
        status: optional
        badges: [optional, enterprise]
        notes: "Enterprise-grade Postgres backup."

  # ==========================================
  # 9) Hanko — Security / Identity / Secrets
  # ==========================================
  - name: Hanko
    description: "The seal — auth, identity, and secrets."
    color_theme: "#2F4F4F"
    rolls:
      - id: hanko.authentik
        name: "Authentik"
        status: recommended
        badges: [popular]
        notes: "Lightweight SSO/IdP."
      - id: hanko.keycloak
        name: "Keycloak"
        status: optional
        badges: [optional, enterprise, heavy]
        notes: "Battle-tested enterprise IdP; heavier footprint."
      - id: hanko.infisical
        name: "Infisical"
        status: recommended
        notes: "Secrets manager for modern stacks."
      - id: hanko.vaultwarden
        name: "Vaultwarden"
        status: recommended
        notes: "Self-hosted Bitwarden-compatible password manager."
      - id: hanko.vault
        name: "HashiCorp Vault"
        status: optional
        badges: [optional, enterprise, heavy]
        notes: "Enterprise secrets + PKI."
      - id: hanko.sops
        name: "SOPS"
        status: recommended
        notes: "Git-friendly secrets encryption (age/GPG)."
      - id: hanko.sealed-secrets
        name: "Sealed Secrets"
        status: optional
        badges: [optional, k8s, future]
        notes: "K8s-native secrets; roadmap."

  # ==============================================
  # 10) Gunkanmaki — High-Performance Inference
  # ==============================================
  - name: Gunkanmaki
    description: "Battleship rolls — high-performance inference."
    color_theme: "#FF4500"
    rolls:
      - id: gunkanmaki.vllm
        name: "vLLM"
        status: recommended
        badges: [popular, gpu]
        notes: "Fast LLM serving with OpenAI/HF compat."
      - id: gunkanmaki.tgi
        name: "Text Generation Inference (TGI)"
        status: recommended
        badges: [gpu]
        notes: "Optimized HuggingFace serving stack."
      - id: gunkanmaki.triton
        name: "NVIDIA Triton Server"
        status: optional
        badges: [optional, enterprise, gpu, heavy]
        notes: "Enterprise GPU inference server."

  # ==========================================
  # 11) Makimono — Collaboration & API Docs
  # ==========================================
  - name: Makimono
    description: "Scroll rolls — collaboration and API docs."
    color_theme: "#708090"
    rolls:
      - id: makimono.gitea
        name: "Gitea"
        status: recommended
        notes: "Lightweight Git hosting with CI/CD."
      - id: makimono.homepage
        name: "Homepage"
        status: recommended
        notes: "Dashboard for services — the kitchen counter."
      - id: makimono.redoc
        name: "Redoc"
        status: recommended
        notes: "Static API documentation generator."
      - id: makimono.swaggerui
        name: "SwaggerUI"
        status: recommended
        notes: "Interactive API explorer/tester."
---

# 🍱 Sushi Kitchen Menu

This page is the **human-friendly catalog** (Styles → Rolls).  
- **Contracts (deps/images/versions/ports/env)** live in `docs/manifest/contracts.yml`.  
- **Combos** live in `docs/manifest/combos.yml`.  
- **Platters** live in `docs/manifest/platters.yml`.  
- **Badge dictionary** lives in `docs/manifest/badges.yml` (icons in `assets/badges/`).  

> Why this split? It prevents drift: copy stays readable, while the resolver/CLI and CI pin images/versions and allocate ports safely.

## 🎯 **Current Status: We're at Phase 0, not Phase 3**

We need to work on **Phase 1** first - creating the generator. Here's what we need to do:

## 🚀 **Let's Start with Step 1: Create the Generator**

I'll create a Python script that can read the manifest files and generate compose configurations. Here's what we need:

```bash
<code_block_to_apply_changes_from>
```

**Would you like me to:**

1. **Create the generator script** that reads your manifest files and outputs compose configurations?
2. **Start by converting one existing compose file** (like `docker-compose.base.yml`) into a template?
3. **Create a simple test** with one platter (like `platter.starter`) to validate the approach?

Which approach would you prefer to start with? I recommend starting with **option 1** - creating the generator script, because once we have that working, we can easily convert the existing files and test with different platters.

The generator will be the foundation that makes everything else possible!
