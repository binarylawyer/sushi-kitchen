---
# ============================================================
# 🍣 Sushi Kitchen — Menu Manifest (SSOT: human-facing catalog)
# Version: 0.1.0  (supersedes 2.5)
# Schema: front matter for website/homepage rendering.
# IMPORTANT:
#  - Keep ONLY presentational fields here (ids, names, notes, badges).
#  - Operational fields (images/versions/ports/env/deps) live in:
#      • docs/manifest/contracts.yml
#      • docs/manifest/combos.yml
#      • docs/manifest/platters.yml
#  - Badge definitions (labels/tooltips/icons) live in:
#      • docs/manifest/badges.yml   (+ SVGs in assets/badges/)
# ============================================================

title: "🍣 Sushi Kitchen Menu Manifest"
version: "0.1.0"
manifest_schema_version: "1.1"
last_updated: 2025-09-16
legend: "✅ recommended · ⚖️ optional"

deployment_targets:
  - docker-compose
  - kubernetes
  - docker-swarm

privacy_profiles_supported:
  - chirashi
  - temaki
  - inari

# Badge keys reference (define details in badges.yml):
# popular, optional, gpu, gpu-optional, enterprise, heavy, experimental, k8s, future, ci

styles:

  # ========================
  # Hosomaki — Core & Inference
  # ========================
  - name: Hosomaki
    description: "Core orchestration & inference you reach for daily."
    color_theme: "#2C3E50"
    rolls:
      - id: hosomaki.n8n
        name: "n8n"
        status: recommended
        badges: [popular]
        notes: "Workflow orchestration & automation."
      - id: hosomaki.litellm
        name: "LiteLLM"
        status: recommended
        badges: [popular]
        notes: "Universal LLM gateway for local + cloud."
      - id: hosomaki.ollama
        name: "Ollama"
        status: recommended
        badges: [popular, gpu-optional]
        notes: "Local LLM engine with a huge community."
      - id: hosomaki.anythingllm
        name: "AnythingLLM"
        status: recommended
        badges: [popular]
        notes: "RAG-first chat interface; quick start for teams."
      - id: hosomaki.vllm
        name: "vLLM"
        status: recommended
        badges: [gpu, popular]
        notes: "Production inference server; OpenAI/HF-compatible."
      - id: hosomaki.caddy
        name: "Caddy"
        status: recommended
        badges: [popular]
        notes: "Modern web server with automatic HTTPS & reverse proxy."
      - id: hosomaki.tgi
        name: "Text Generation Inference (TGI)"
        status: optional
        badges: [optional, gpu]
        notes: "Optimized Hugging Face generation stack."
      - id: hosomaki.triton
        name: "NVIDIA Triton Inference Server"
        status: optional
        badges: [optional, gpu, enterprise, heavy]
        notes: "Enterprise GPU inference for multi-framework serving."
      - id: hosomaki.temporal
        name: "Temporal"
        status: optional
        badges: [optional]
        notes: "Durable workflow orchestration for critical jobs."

  # ===========================================
  # Futomaki — Databases, Knowledge & Storage
  # ===========================================
  - name: Futomaki
    description: "The filling: databases, vector/graph stores, and storage."
    color_theme: "#27AE60"
    rolls:
      - id: futomaki.supabase
        name: "Supabase"
        status: recommended
        badges: [popular]
        notes: "Postgres-as-a-service with auth & realtime."
      - id: futomaki.postgres
        name: "PostgreSQL + pgvector"
        status: recommended
        badges: [popular]
        notes: "Data foundation with vector similarity search."
      - id: futomaki.redis
        name: "Redis"
        status: recommended
        notes: "Caching, queues, rate-limits; glue for async."
      - id: futomaki.qdrant
        name: "Qdrant"
        status: recommended
        badges: [popular]
        notes: "High-performance vector DB for RAG."
      - id: futomaki.weaviate
        name: "Weaviate"
        status: optional
        badges: [optional, enterprise]
        notes: "GraphQL-native vector DB; enterprise-leaning."
      - id: futomaki.chroma
        name: "Chroma"
        status: optional
        badges: [optional]
        notes: "Simple vector store for prototyping."
      - id: futomaki.infinity
        name: "Infinity (Embeddings)"
        status: optional
        badges: [optional]
        notes: "Fast embedding server for sentence-transformers."
      - id: futomaki.neo4j
        name: "Neo4j"
        status: recommended
        notes: "Graph database powerhouse (GraphRAG, knowledge graphs)."
      - id: futomaki.minio
        name: "MinIO"
        status: recommended
        notes: "S3-compatible object storage for artifacts/media."
      - id: futomaki.restic
        name: "Restic"
        status: recommended
        notes: "Encrypted, deduplicated backups for peace of mind."
      - id: futomaki.pgadmin
        name: "pgAdmin"
        status: recommended
        notes: "Web UI for Postgres administration."
      - id: futomaki.redisinsight
        name: "RedisInsight"
        status: optional
        badges: [optional]
        notes: "GUI for Redis monitoring and queries."
      - id: futomaki.rclone-browser
        name: "Rclone Browser"
        status: optional
        badges: [optional]
        notes: "GUI for rclone operations."

  # ==========================================
  # Nigiri — Speech & Interaction
  # ==========================================
  - name: Nigiri
    description: "Clean, direct interaction: ASR, TTS, and chat UIs."
    color_theme: "#E74C3C"
    rolls:
      - id: nigiri.whisper
        name: "Whisper"
        status: recommended
        badges: [gpu-optional]
        notes: "Near human-level ASR; local and server modes."
      - id: nigiri.piper
        name: "Piper"
        status: recommended
        notes: "Lightweight, fast TTS."
      - id: nigiri.openvoice
        name: "OpenVoice"
        status: optional
        badges: [optional, experimental]
        notes: "Voice cloning; early-stage—handle with care."
      - id: nigiri.open-webui
        name: "Open WebUI"
        status: optional
        badges: [optional, popular]
        notes: "Popular Ollama/LLM chat UI."

  # ================================================
  # Uramaki — Visual & Media Generation/Processing
  # ================================================
  - name: Uramaki
    description: "Inside-out creativity: image/video generation & tooling."
    color_theme: "#9B59B6"
    rolls:
      - id: uramaki.comfyui
        name: "ComfyUI"
        status: recommended
        badges: [popular, gpu]
        notes: "Node-based Stable Diffusion pipelines."
      - id: uramaki.automatic1111
        name: "Automatic1111"
        status: optional
        badges: [optional, gpu]
        notes: "Stable Diffusion WebUI."
      - id: uramaki.ffmpeg
        name: "FFmpeg"
        status: recommended
        notes: "Swiss-army knife for audio/video processing."
      - id: uramaki.imagemagick
        name: "ImageMagick"
        status: recommended
        notes: "Classic image manipulation toolkit."
      - id: uramaki.rclone
        name: "rclone"
        status: recommended
        notes: "Sync media/artifacts to S3/MinIO/GDrive."
      - id: uramaki.remotion
        name: "Remotion"
        status: optional
        badges: [optional]
        notes: "Programmatic video creation."

  # =========================================
  # Chirashi — Data Science & Compute
  # =========================================
  - name: Chirashi
    description: "Exploratory bowls: notebooks, dashboards, compute."
    color_theme: "#1ABC9C"
    rolls:
      - id: chirashi.jupyterlab
        name: "JupyterLab"
        status: recommended
        notes: "Interactive notebooks for DS/AI."
      - id: chirashi.panel
        name: "Panel"
        status: optional
        badges: [optional]
        notes: "Dashboard creation from notebooks."
      - id: chirashi.dask
        name: "Dask"
        status: optional
        badges: [optional, heavy]
        notes: "Parallel computing framework."
      - id: chirashi.mlflow
        name: "MLflow"
        status: recommended
        notes: "Experiment tracking & model registry."
      - id: chirashi.bentoml
        name: "BentoML"
        status: optional
        badges: [optional]
        notes: "Model serving framework."
      - id: chirashi.kubeflow
        name: "Kubeflow"
        status: optional
        badges: [optional, enterprise, k8s, future, heavy]
        notes: "End-to-end ML workflows on K8s."
      - id: chirashi.metabase
        name: "Metabase"
        status: optional
        badges: [optional]
        notes: "Analytics & dashboarding."

  # ==================================
  # Temaki — Developer / Builder Tools
  # ==================================
  - name: Temaki
    description: "Hand-rolled builder tools and low-code frameworks."
    color_theme: "#34495E"
    rolls:
      - id: temaki.vscode-server
        name: "VS Code Server"
        status: recommended
        notes: "Full IDE in the browser."
      - id: temaki.gitea
        name: "Gitea"
        status: optional
        badges: [optional]
        notes: "Self-hosted Git service with CI/CD."
      - id: temaki.sonarqube
        name: "SonarQube"
        status: optional
        badges: [optional, ci]
        notes: "Code quality & vulnerability scanning."
      - id: temaki.flowise
        name: "Flowise"
        status: optional
        badges: [optional]
        notes: "Visual flow/agent builder."
      - id: temaki.dify
        name: "Dify"
        status: optional
        badges: [optional]
        notes: "Open-source assistant builder."
      - id: temaki.windmill
        name: "Windmill"
        status: optional
        badges: [optional]
        notes: "Workflow/scheduling/ETL builder."
      - id: temaki.openui
        name: "OpenUI"
        status: optional
        badges: [optional, experimental]
        notes: "Conversational UI prototyping."

  # ==========================================
  # Inari — Observability & Telemetry
  # ==========================================
  - name: Inari
    description: "Seeing the whole kitchen: metrics, logs, traces, LLM QA."
    color_theme: "#F39C12"
    rolls:
      - id: inari.prometheus
        name: "Prometheus"
        status: recommended
        notes: "Metrics collection standard."
      - id: inari.grafana
        name: "Grafana"
        status: recommended
        notes: "Dashboards and observability hub."
      - id: inari.langfuse
        name: "Langfuse"
        status: recommended
        notes: "LLM tracing/analytics."
      - id: inari.cadvisor
        name: "cAdvisor"
        status: recommended
        notes: "Container-level resource metrics."
      - id: inari.node-exporter
        name: "Node Exporter"
        status: recommended
        notes: "Host/system metrics exporter."
      - id: inari.loki
        name: "Loki"
        status: optional
        badges: [optional]
        notes: "Log aggregation (Grafana stack)."
      - id: inari.promtail
        name: "Promtail"
        status: optional
        badges: [optional]
        notes: "Log shipper; pairs with Loki."
      - id: inari.otel-collector
        name: "OpenTelemetry Collector"
        status: optional
        badges: [optional]
        notes: "Unified telemetry ingestion (traces/metrics/logs)."

  # ==========================================
  # Gunkanmaki — Security, Identity & Protection
  # ==========================================
  - name: Gunkanmaki
    description: "Armored vessels: identity, secrets, and access."
    color_theme: "#FF4500"
    rolls:
      - id: gunkanmaki.authentik
        name: "Authentik"
        status: recommended
        badges: [popular]
        notes: "Lightweight SSO/IdP."
      - id: gunkanmaki.keycloak
        name: "Keycloak"
        status: optional
        badges: [optional, enterprise, heavy]
        notes: "Battle-tested enterprise IdP."
      - id: gunkanmaki.vaultwarden
        name: "Vaultwarden"
        status: recommended
        notes: "Self-hosted Bitwarden-compatible passwords."
      - id: gunkanmaki.infisical
        name: "Infisical"
        status: recommended
        notes: "Secrets/config manager for modern stacks."

  # ==========================================
  # Sashimi — API & Documentation
  # ==========================================
  - name: Sashimi
    description: "Clean slices: docs sites and API explorers."
    color_theme: "#708090"
    rolls:
      - id: sashimi.docusaurus
        name: "Docusaurus"
        status: recommended
        notes: "Documentation site generator."
      - id: sashimi.swaggerui
        name: "Swagger UI"
        status: recommended
        notes: "Interactive API explorer/tester."
      - id: sashimi.redoc
        name: "Redoc"
        status: recommended
        notes: "Static API documentation generator."

  # ==========================================
  # Otsumami — Optional Side Utilities
  # ==========================================
  - name: Otsumami
    description: "Snacks & niceties used occasionally but not required."
    color_theme: "#8B4513"
    rolls:
      - id: otsumami.duckdb
        name: "DuckDB"
        status: optional
        badges: [optional, popular]
        notes: "'SQLite for OLAP'—fast local analytics."
      - id: otsumami.sqlite
        name: "SQLite"
        status: optional
        badges: [optional]
        notes: "Ubiquitous embedded relational DB."
      - id: otsumami.searxng
        name: "SearXNG"
        status: optional
        badges: [optional]
        notes: "Privacy-focused search engine aggregator."

enterprise_and_deployment:
  omakase_mode: "Automatic optimal stack / curated combo."
  kaiseki_mode: "Premium curated / high-performance alternatives."
  exports: ["Kubernetes/Helm", "Docker Swarm", "Ansible", "Bare-metal"]
---

## 🍱 Sushi Kitchen Menu (human-facing)

This is the **catalog** (Styles → Rolls).

- **Contracts (deps/images/versions/ports/env)** → `docs/manifest/contracts.yml`
- **Combos** → `docs/manifest/combos.yml`
- **Platters** → `docs/manifest/platters.yml`
- **Badges** → `docs/manifest/badges.yml` (icons in `assets/badges/`)

Meet our chefs: **Port** and **Starboard**.

- **Port's sushi** = core foundation you'll use daily (Hosomaki, Futomaki, Uramaki, Nigiri, Temaki, Gunkanmaki, Sashimi).
- **Starboard's bowls/specialties** = exploratory, observability, and feasts (Chirashi, Inari, Otsumami, plus Omakase/Kaiseki).

> "Every roll has its place; every bowl adds richness."
