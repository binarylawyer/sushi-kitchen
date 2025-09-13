---
title: "🍣 Sushi Kitchen Menu Manifest"
version: "0.2.2"
last_updated: 2025-09-11
legend: "✅ recommended · ⚖️ optional"
manifest_schema_version: "1.0"

styles:
  - name: Hosomaki
    description: "Thin rolls — the core foundation."
    color_theme: "#2C3E50"
    port_range: "3000-3009"
    rolls:
      - id: hosomaki.ollama
        name: "Ollama"
        status: recommended
        badges: [popular, gpu-optional]
        notes: "Local LLM engine with huge community traction."
        version: "0.1.44"
        docker_image: "ollama/ollama"
        
      - id: hosomaki.litellm
        name: "LiteLLM"
        status: recommended
        badges: [popular]
        notes: "Universal API gateway for local + cloud LLMs."
        version: "1.0.0"
        docker_image: "ghcr.io/berriai/litellm"
        
      - id: hosomaki.n8n
        name: "n8n"
        status: recommended
        badges: [popular]
        notes: "Workflow automation/orchestration brain."
        version: "1.0.0"
        docker_image: "n8nio/n8n"
        
      - id: hosomaki.supabase
        name: "Supabase"
        status: recommended
        badges: [popular]
        notes: "Postgres + pgvector backend with auth & realtime."
        version: "latest"
        docker_image: "supabase/postgres"
        
      - id: hosomaki.redis
        name: "Redis"
        status: recommended
        notes: "Cache & queue; speeds async tasks."
        version: "7-alpine"
        docker_image: "redis"
        
      - id: hosomaki.caddy
        name: "Caddy"
        status: recommended
        notes: "Modern reverse proxy with automatic HTTPS."
        version: "2-alpine"
        docker_image: "caddy"
        
      - id: hosomaki.portainer
        name: "Portainer"
        status: optional
        badges: [optional]
        notes: "Optional Docker GUI for homelab visibility."
        version: "latest"
        docker_image: "portainer/portainer-ce"

  - name: Futomaki
    description: "Fat rolls — knowledge stores, RAG, and graphs."
    color_theme: "#27AE60"
    port_range: "3010-3019"
    rolls:
      - id: futomaki.qdrant
        name: "Qdrant"
        status: recommended
        badges: [popular]
        notes: "High-performance vector database for RAG."
        version: "latest"
        docker_image: "qdrant/qdrant"
        
      - id: futomaki.chroma
        name: "Chroma"
        status: recommended
        notes: "Simple prototyping vector store."
        version: "latest"
        docker_image: "ghcr.io/chroma-core/chroma"
        
      - id: futomaki.weaviate
        name: "Weaviate"
        status: optional
        badges: [optional, enterprise]
        notes: "GraphQL-native vector DB; enterprise-leaning alternative."
        version: "latest"
        docker_image: "semitechnologies/weaviate"
        
      - id: futomaki.neo4j
        name: "Neo4j"
        status: recommended
        notes: "Graph database powerhouse — great for GraphRAG."
        version: "5"
        docker_image: "neo4j"
        
      - id: futomaki.memgraph
        name: "Memgraph"
        status: optional
        badges: [optional]
        notes: "In-memory graph DB; niche alternative."
        version: "latest"
        docker_image: "memgraph/memgraph"
        
      - id: futomaki.arangodb
        name: "ArangoDB"
        status: optional
        badges: [optional, heavy]
        notes: "Multi-model DB (graph+doc+KV); heavier footprint."
        version: "latest"
        docker_image: "arangodb/arangodb"
        
      - id: futomaki.anythingllm
        name: "AnythingLLM"
        status: recommended
        badges: [popular]
        notes: "Turnkey RAG UI with strong community."
        version: "latest"
        docker_image: "mintplexlabs/anythingllm"
        
      - id: futomaki.infinity
        name: "Infinity (Embeddings)"
        status: recommended
        notes: "Fast embedding server for sentence transformers."
        version: "latest"
        docker_image: "michaelf34/infinity"
        
      - id: futomaki.flowise
        name: "Flowise"
        status: optional
        badges: [optional]
        notes: "Visual LangChain builder; no-code agent graphs."
        version: "latest"
        docker_image: "flowiseai/flowise"
        
      - id: futomaki.dify
        name: "Dify"
        status: optional
        badges: [optional]
        notes: "LangSmith-style orchestration; OSS flavor."
        version: "latest"
        docker_image: "langgenius/dify-api"

  - name: Temaki
    description: "Hand rolls — voice, interaction, and conversation."
    color_theme: "#E74C3C"
    port_range: "3020-3029"
    rolls:
      - id: temaki.whisper
        name: "Whisper"
        status: recommended
        badges: [gpu-optional]
        notes: "ASR with near human-level accuracy."
        version: "latest"
        docker_image: "onerahmet/openai-whisper-asr-webservice"
        
      - id: temaki.piper
        name: "Piper"
        status: recommended
        notes: "Lightweight text-to-speech."
        version: "latest"
        docker_image: "rhasspy/piper"
        
      - id: temaki.openvoice
        name: "OpenVoice"
        status: optional
        badges: [optional, experimental]
        notes: "Voice cloning; early-stage expectations."
        version: "latest"
        docker_image: "ghcr.io/myshell-ai/openvoice"
        
      - id: temaki.openui
        name: "OpenUI"
        status: optional
        badges: [optional, experimental]
        notes: "Experimental UI generator for conversational apps."
        version: "latest"
        docker_image: "ghcr.io/wandb/openui"
        
      - id: temaki.open-webui
        name: "Open WebUI"
        status: recommended
        badges: [popular]
        notes: "Popular Ollama/LLM chat UI."
        version: "latest"
        docker_image: "ghcr.io/open-webui/open-webui"
        
      - id: temaki.adorable-clone
        name: "Adorable.dev (clone)"
        status: optional
        badges: [optional, experimental]
        notes: "In-house playful UI alternative."
        version: "latest"
        docker_image: "sushi-kitchen/adorable-clone"

  - name: Uramaki
    description: "Inside-out rolls — creative, visual, and media."
    color_theme: "#9B59B6"
    port_range: "3030-3039"
    rolls:
      - id: uramaki.comfyui
        name: "ComfyUI"
        status: recommended
        badges: [popular, gpu]
        notes: "Node-based Stable Diffusion pipelines; GPU recommended."
        version: "latest"
        docker_image: "yanwk/comfyui-boot"
        
      - id: uramaki.ffmpeg
        name: "FFmpeg"
        status: recommended
        notes: "Swiss-army knife for audio/video processing."
        version: "latest"
        docker_image: "jrottenberg/ffmpeg"
        
      - id: uramaki.remotion
        name: "Remotion"
        status: optional
        badges: [optional]
        notes: "Programmatic video generation."
        version: "latest"
        docker_image: "remotion/remotion"
        
      - id: uramaki.scanned
        name: "Scanned"
        status: optional
        badges: [optional, experimental]
        notes: "Video analysis utilities; early stage."
        version: "latest"
        docker_image: "ghcr.io/scanned/scanned"
        
      - id: uramaki.rclone
        name: "rclone"
        status: recommended
        notes: "Sync to S3/MinIO/GDrive; storage glue."
        version: "latest"
        docker_image: "rclone/rclone"
        
      - id: uramaki.imagemagick
        name: "ImageMagick"
        status: recommended
        notes: "Classic image manipulation toolkit."
        version: "latest"
        docker_image: "dpokidov/imagemagick"

  - name: Dragon Roll
    description: "Oversight — observability, logs, tracing, quality."
    color_theme: "#F39C12"
    port_range: "3040-3049"
    rolls:
      - id: dragon.prometheus
        name: "Prometheus"
        status: recommended
        notes: "Metrics collection standard."
        version: "latest"
        docker_image: "prom/prometheus"
        
      - id: dragon.grafana
        name: "Grafana"
        status: recommended
        notes: "Dashboards and observability hub."
        version: "latest"
        docker_image: "grafana/grafana"
        
      - id: dragon.cadvisor
        name: "cAdvisor"
        status: recommended
        notes: "Container-level resource metrics."
        version: "latest"
        docker_image: "gcr.io/cadvisor/cadvisor"
        
      - id: dragon.langfuse
        name: "Langfuse"
        status: recommended
        notes: "LLM tracing/analytics."
        version: "latest"
        docker_image: "langfuse/langfuse"
        
      - id: dragon.otel-collector
        name: "OpenTelemetry Collector"
        status: recommended
        notes: "Unified telemetry ingestion."
        version: "latest"
        docker_image: "otel/opentelemetry-collector"
        
      - id: dragon.loki
        name: "Loki"
        status: optional
        badges: [optional]
        notes: "Log aggregation (Grafana stack)."
        version: "latest"
        docker_image: "grafana/loki"
        
      - id: dragon.promtail
        name: "Promtail"
        status: optional
        badges: [optional]
        notes: "Log shipper; pairs with Loki."
        version: "latest"
        docker_image: "grafana/promtail"
        
      - id: dragon.sonarqube
        name: "SonarQube"
        status: optional
        badges: [optional, ci]
        notes: "Code quality/vulnerability scanning (dev/CI focus)."
        version: "lts-community"
        docker_image: "sonarqube"
        
      - id: dragon.istio
        name: "Istio"
        status: optional
        badges: [optional, enterprise, k8s, future]
        notes: "Service mesh; enterprise/K8s roadmap."
        version: "latest"
        docker_image: "istio/pilot"
        
      - id: dragon.traefik
        name: "Traefik"
        status: optional
        badges: [optional, enterprise, future]
        notes: "Alt reverse proxy; enterprise futures."
        version: "latest"
        docker_image: "traefik"

  - name: Tamago
    description: "Egg — developer tools, simple yet skilled."
    color_theme: "#1ABC9C"
    port_range: "3050-3059"
    rolls:
      - id: tamago.vscode-server
        name: "VS Code Server"
        status: recommended
        notes: "Web IDE in the browser."
        version: "latest"
        docker_image: "codercom/code-server"
        
      - id: tamago.jupyterlab
        name: "JupyterLab"
        status: recommended
        notes: "Notebook environment for DS/AI."
        version: "latest"
        docker_image: "jupyter/datascience-notebook"
        
      - id: tamago.panel
        name: "Panel"
        status: optional
        badges: [optional]
        notes: "Lightweight dashboarding for data apps."
        version: "latest"
        docker_image: "pyviz/panel"
        
      - id: tamago.dask
        name: "Dask"
        status: optional
        badges: [optional, heavy]
        notes: "Parallel computing; heavier footprint."
        version: "latest"
        docker_image: "daskdev/dask"
        
      - id: tamago.docusaurus
        name: "Docusaurus"
        status: recommended
        notes: "Docs site generator."
        version: "latest"
        docker_image: "node:18-alpine"
        
      - id: tamago.duckdb
        name: "DuckDB"
        status: optional
        badges: [optional, popular]
        notes: "Fast analytics DB — 'SQLite for OLAP'."
        version: "latest"
        docker_image: "duckdb/duckdb"
        
      - id: tamago.sqlite
        name: "SQLite"
        status: optional
        badges: [optional]
        notes: "Ubiquitous embedded relational DB."
        version: "latest"
        docker_image: "alpine/sqlite"

  - name: Spider Roll
    description: "Intricate — MLOps, experiments, orchestration."
    color_theme: "#34495E"
    port_range: "3060-3069"
    rolls:
      - id: spider.mlflow
        name: "MLflow"
        status: recommended
        notes: "Track experiments, metrics, and artifacts."
        version: "latest"
        docker_image: "python:3.9"
        
      - id: spider.ray
        name: "Ray"
        status: optional
        badges: [optional, heavy]
        notes: "Distributed training/serving; heavy but powerful."
        version: "latest"
        docker_image: "rayproject/ray"
        
      - id: spider.bentoml
        name: "BentoML"
        status: optional
        badges: [optional]
        notes: "Model serving/deployment toolkit."
        version: "latest"
        docker_image: "bentoml/bentoml"
        
      - id: spider.kubeflow
        name: "Kubeflow"
        status: optional
        badges: [optional, enterprise, k8s, future, heavy]
        notes: "End-to-end ML pipelines; enterprise/K8s roadmap."
        version: "latest"
        docker_image: "kubeflownotebookswg/jupyter-scipy"
        
      - id: spider.temporal
        name: "Temporal"
        status: optional
        badges: [optional]
        notes: "Durable workflow orchestration."
        version: "latest"
        docker_image: "temporalio/temporal"

  - name: Shoyu
    description: "Soy sauce — storage, backup, data lifecycle."
    color_theme: "#8B4513"
    port_range: "3070-3079"
    rolls:
      - id: shoyu.minio
        name: "MinIO"
        status: recommended
        notes: "S3-compatible object storage."
        version: "latest"
        docker_image: "minio/minio"
        
      - id: shoyu.restic
        name: "Restic"
        status: recommended
        notes: "Encrypted, deduplicated backups."
        version: "latest"
        docker_image: "restic/restic"
        
      - id: shoyu.duplicati
        name: "Duplicati"
        status: optional
        badges: [optional]
        notes: "GUI backup; simpler flows."
        version: "latest"
        docker_image: "duplicati/duplicati"
        
      - id: shoyu.pgadmin
        name: "pgAdmin"
        status: recommended
        notes: "Web UI for Postgres."
        version: "latest"
        docker_image: "dpage/pgadmin4"
        
      - id: shoyu.redisinsight
        name: "RedisInsight"
        status: optional
        badges: [optional]
        notes: "GUI for Redis monitoring/queries."
        version: "latest"
        docker_image: "redislabs/redisinsight"
        
      - id: shoyu.borgbackup
        name: "BorgBackup"
        status: optional
        badges: [optional]
        notes: "Efficient dedup backups."
        version: "latest"
        docker_image: "borgbackup/borg"
        
      - id: shoyu.pgbackrest
        name: "pgBackRest"
        status: optional
        badges: [optional, enterprise]
        notes: "Enterprise-grade Postgres backup."
        version: "latest"
        docker_image: "pgbackrest/pgbackrest"

  - name: Hanko
    description: "The seal — auth, identity, and secrets."
    color_theme: "#2F4F4F"
    port_range: "3080-3089"
    rolls:
      - id: hanko.authentik
        name: "Authentik"
        status: recommended
        badges: [popular]
        notes: "Lightweight SSO/IdP."
        version: "latest"
        docker_image: "ghcr.io/goauthentik/server"
        
      - id: hanko.keycloak
        name: "Keycloak"
        status: optional
        badges: [optional, enterprise, heavy]
        notes: "Battle-tested enterprise IdP; heavier footprint."
        version: "latest"
        docker_image: "quay.io/keycloak/keycloak"
        
      - id: hanko.infisical
        name: "Infisical"
        status: recommended
        notes: "Secrets manager for modern stacks."
        version: "latest"
        docker_image: "infisical/infisical"
        
      - id: hanko.vaultwarden
        name: "Vaultwarden"
        status: recommended
        notes: "Self-hosted Bitwarden-compatible password manager."
        version: "latest"
        docker_image: "vaultwarden/server"
        
      - id: hanko.vault
        name: "HashiCorp Vault"
        status: optional
        badges: [optional, enterprise, heavy]
        notes: "Enterprise secrets + PKI."
        version: "latest"
        docker_image: "vault"
        
      - id: hanko.sops
        name: "SOPS"
        status: recommended
        notes: "Git-friendly secrets encryption (age/GPG)."
        version: "latest"
        docker_image: "mozilla/sops"
        
      - id: hanko.sealed-secrets
        name: "Sealed Secrets"
        status: optional
        badges: [optional, k8s, future]
        notes: "K8s-native secrets; roadmap."
        version: "latest"
        docker_image: "bitnami/sealed-secrets-controller"

  - name: Gunkanmaki
    description: "Battleship rolls — high-performance inference."
    color_theme: "#FF4500"
    port_range: "3090-3099"
    rolls:
      - id: gunkanmaki.vllm
        name: "vLLM"
        status: recommended
        badges: [popular, gpu]
        notes: "Fast LLM serving with OpenAI/HF compat."
        version: "latest"
        docker_image: "vllm/vllm-openai"
        
      - id: gunkanmaki.tgi
        name: "Text Generation Inference (TGI)"
        status: recommended
        badges: [gpu]
        notes: "Optimized HuggingFace serving stack."
        version: "latest"
        docker_image: "ghcr.io/huggingface/text-generation-inference"
        
      - id: gunkanmaki.triton
        name: "NVIDIA Triton Server"
        status: optional
        badges: [optional, enterprise, gpu, heavy]
        notes: "Enterprise GPU inference server."
        version: "latest"
        docker_image: "nvcr.io/nvidia/tritonserver"

  - name: Makimono
    description: "Scroll rolls — collaboration and API docs."
    color_theme: "#708090"
    port_range: "3100-3109"
    rolls:
      - id: makimono.gitea
        name: "Gitea"
        status: recommended
        notes: "Lightweight Git hosting with CI/CD."
        version: "latest"
        docker_image: "gitea/gitea"
        
      - id: makimono.homepage
        name: "Homepage"
        status: recommended
        notes: "Dashboard for services — the kitchen counter."
        version: "latest"
        docker_image: "ghcr.io/gethomepage/homepage"
        
      - id: makimono.redoc
        name: "Redoc"
        status: recommended
        notes: "Static API documentation generator."
        version: "latest"
        docker_image: "redocly/redoc"
        
      - id: makimono.swaggerui
        name: "SwaggerUI"
        status: recommended
        notes: "Interactive API explorer/tester."
        version: "latest"
        docker_image: "swaggerapi/swagger-ui"

badge_definitions:
  popular:
    label: "Popular"
    color: "#28A745"
    tooltip: "High community adoption and active maintenance"
  optional:
    label: "Optional"
    color: "#6C757D"
    tooltip: "Not required for most builds; enable for specific needs"
  gpu:
    label: "GPU Required"
    color: "#FF6B35"
    tooltip: "Requires CUDA-capable GPU for optimal performance"
  gpu-optional:
    label: "GPU Optional"
    color: "#FFA500"
    tooltip: "Runs on CPU but significantly faster with GPU"
  enterprise:
    label: "Enterprise"
    color: "#17A2B8"
    tooltip: "Best for enterprise deployments; heavier resource requirements"
  heavy:
    label: "Heavy"
    color: "#DC3545"
    tooltip: "High resource requirements; ensure adequate hardware"
  experimental:
    label: "Experimental"
    color: "#FFC107"
    tooltip: "Early-stage; expect potential breaking changes"
  k8s:
    label: "Kubernetes"
    color: "#326CE5"
    tooltip: "Designed for Kubernetes; advanced orchestration"
  future:
    label: "Roadmap"
    color: "#868E96"
    tooltip: "Planned for future versions; subject to change"
  ci:
    label: "CI/CD"
    color: "#20C997"
    tooltip: "Primarily used in development and CI/CD workflows"

deployment_targets:
  - docker-compose
  - kubernetes
  - docker-swarm

privacy_profiles_supported:
  - chirashi
  - temaki
  - inari
---

# 🍱 Sushi Kitchen Menu

This is the master menu catalog with 50+ curated AI infrastructure services organized into 11 intuitive "sushi styles."

For dependency logic, see `contracts.yml`; for curated bundles, see `combos.yml`; for full environments, see `platters.yml`.

## Quick Reference

- **✅ Recommended**: Battle-tested, high adoption, essential for most builds
- **⚖️ Optional**: Specialized use cases, alternatives, or experimental

## 🍣 Styles Overview

1. **Hosomaki** (Foundation) - Essential core services  
2. **Futomaki** (Knowledge) - RAG, vector databases, knowledge management  
3. **Temaki** (Voice) - Speech, audio, conversational interfaces  
4. **Uramaki** (Visual) - Image, video, creative generation  
5. **Dragon Roll** (Observability) - Monitoring, logging, tracing  
6. **Tamago** (Dev Tools) - IDEs, notebooks, development environment  
7. **Spider Roll** (MLOps) - Experiment tracking, model deployment  
8. **Shoyu** (Storage) - Databases, backups, data management  
9. **Hanko** (Security) - Authentication, secrets, compliance  
10. **Gunkanmaki** (Performance) - High-speed inference engines  
11. **Makimono** (Collaboration) - Git, documentation, team tools

---

*Total: 54 rolls across 11 styles*  
*Version 0.2.2 | Ready for production deployment*