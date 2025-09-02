# Sushi Rolls (Compose Profiles)

- **hosomaki** – core: Ollama, n8n, LiteLLM, Postgres+pgvector, Qdrant, Redis, Caddy, Homepage, MinIO.
- **futomaki** – RAG/data: Qdrant/Weaviate (pick one), Neo4j (opt-in).
- **temaki** – voice: Whisper ASR, Piper TTS.
- **uramaki** – images: ComfyUI.
- **dragon** – observability: Prometheus, Grafana, Langfuse, (Loki/Promtail optional).
- **tamago** – dev tools: VS Code Server, (Jupyter optional).
- **gunkanmaki** – high-perf inference: vLLM (cloud/local GPU).
- **spider** – MLOps: MLflow.
- **cloud** – override only: point local routers to remote GPU endpoints; adds no services.
