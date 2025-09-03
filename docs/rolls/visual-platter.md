# 🍱 Sushi Kitchen Platter Map

```mermaid
graph TD
  subgraph Hosomaki[Hosomaki Combo]
    n8n[n8n] --> supabase[Supabase]
    supabase --> postgres[Postgres]
    postgres --> redis[Redis]
    redis --> minio[MinIO]
    minio --> qdrant[Qdrant]
    qdrant --> ollama[Ollama]
  end

  subgraph Futomaki[Futomaki Combo]
    neo4j[Neo4j] --> weaviate[Weaviate]
    weaviate --> chroma[Chroma]
    chroma --> infinity[Infinity]
  end

  subgraph Nigiri[Nigiri Combo]
    litellm[LiteLLM] --> whisper[Whisper]
    whisper --> piper[Piper]
    piper --> comfyui[ComfyUI]
  end

  subgraph Observability[Observability Combo]
    prometheus[Prometheus] --> grafana[Grafana]
    grafana --> cadvisor[cAdvisor]
    cadvisor --> nodeexporter[Node Exporter]
    grafana --> langfuse[Langfuse]
    langfuse --> loki[Loki-Promtail]
  end

  subgraph Security[Security Combo]
    authentik[Authentik] --> caddy[Caddy Forward Auth]
    caddy --> infisical[Infisical]
    infisical --> vault[Vault]
  end

  subgraph Backups[Backups Combo]
    borgmatic[Borgmatic] --> pgbackrest[pgBackRest]
    pgbackrest --> neo4jbackup[Neo4j Admin Backup]
  end
