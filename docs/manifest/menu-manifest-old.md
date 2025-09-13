---
title: "🍣 Sushi Kitchen Menu Manifest"
version: "0.2.2"
last_updated: 2025-09-11
legend: "✅ recommended · ⚖️ optional"
styles:
  - name: Hosomaki
    description: "Thin rolls — the core foundation."
    rolls:
      - id: hosomaki.ollama
        name: "Ollama"
        status: recommended
        badges: [popular]
        notes: "Local LLM engine with a huge community."
      - id: hosomaki.litellm
        name: "LiteLLM"
        status: recommended
        badges: [popular]
        notes: "Universal API gateway for local + cloud LLMs."
      - id: hosomaki.n8n
        name: "n8n"
        status: recommended
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

  - name: Futomaki
    description: "Fat rolls — knowledge stores, RAG, and graphs."
    rolls:
      - id: futomaki.qdrant
        name: "Qdrant"
        status: recommended
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

  - name: Temaki
    description: "Hand rolls — voice, interaction, and conversation."
    rolls:
      - id: temaki.whisper
        name: "Whisper"
        status: recommended
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

  - name: Uramaki
    description: "Inside-out rolls — creative, visual, and media."
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

  - name: Dragon Roll
    description: "Oversight — observability, logs, tracing, quality."
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
        notes: "Service mesh; enterprise/K8s roadmap."
      - id: dragon.traefik
        name: "Traefik"
        status: optional
        badges: [optional, enterprise, future]
        notes: "Alt reverse proxy; enterprise futures."

  - name: Tamago
    description: "Egg — developer tools, simple yet skilled."
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

  - name: Spider Roll
    description: "Intricate — MLOps, experiments, orchestration."
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

  - name: Shoyu
    description: "Soy sauce — storage, backup, data lifecycle."
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

  - name: Hanko
    description: "The seal — auth, identity, and secrets."
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

  - name: Gunkanmaki
    description: "Battleship rolls — high-performance inference."
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

  - name: Makimono
    description: "Scroll rolls — collaboration and API docs."
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
This page is the human-friendly catalog. For dependency logic, see `contracts.yml`; for curated bundles, see `combos.yml`; for full environments, see `platters.yml`.
