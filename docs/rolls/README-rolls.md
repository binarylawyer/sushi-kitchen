# 🍣 Sushi Kitchen Rolls

This is the master index of all rolls in the Sushi Kitchen. 
Each roll has its own page under `docs/rolls/`.

## Hosomaki Combo (Core Rolls)

- [N8n](./n8n.md)
- [Supabase](./supabase.md)
- [Postgres](./postgres.md)
- [Redis](./redis.md)
- [Minio](./minio.md)
- [Qdrant](./qdrant.md)
- [Ollama](./ollama.md)

## Futomaki Combo (Big Data Rolls)

- [Neo4j](./neo4j.md)
- [Weaviate](./weaviate.md)
- [Chroma](./chroma.md)
- [Infinity](./infinity.md)

## Nigiri Combo (AI/ML Specialties)

- [Litellm](./litellm.md)
- [Whisper](./whisper.md)
- [Piper](./piper.md)
- [Comfyui](./comfyui.md)

## Side Dishes (Tools & Utilities)

- [Rclone](./rclone.md)
- [Jupyterlab](./jupyterlab.md)
- [Vscode-server](./vscode-server.md)
- [Homepage](./homepage.md)

## Condiments (Consoles & Browsers)

- [Minio-console](./minio-console.md)
- [Qdrant-console](./qdrant-console.md)
- [Neo4j-browser](./neo4j-browser.md)
- [Sushi-doctor](./sushi-doctor.md)

## Observability Combo (Metrics & Logs)

- [Prometheus](./prometheus.md)
- [Grafana](./grafana.md)
- [Cadvisor](./cadvisor.md)
- [Node-exporter](./node-exporter.md)
- [Langfuse](./langfuse.md)
- [Loki-promtail](./loki-promtail.md)

## Security Combo (Auth & Secrets)

- [Authentik](./authentik.md)
- [Caddy-forward-auth](./caddy-forward-auth.md)
- [Infisical](./infisical.md)
- [Vault](./vault.md)

## Backups Combo (Data Safety)

- [Borgmatic](./borgmatic.md)
- [Pgbackrest](./pgbackrest.md)
- [Neo4j-admin-backup](./neo4j-admin-backup.md)

# 🍣 Sushi Kitchen Rolls

This is the **master index** of all rolls in the Sushi Kitchen.  
Each roll has its own page under `docs/rolls/`.  
Think of this as the **menu cover** — you can browse the platters below and click into each roll for the full recipe.  

---

## 🍱 Visual Platter Map

```mermaid
graph TD
  subgraph Hosomaki[Hosomaki Combo 🍣 Core Rolls]
    n8n([N8n]) --> supabase([Supabase])
    supabase --> postgres([Postgres])
    postgres --> redis([Redis])
    redis --> minio([MinIO])
    minio --> qdrant([Qdrant])
    qdrant --> ollama([Ollama])
  end

  subgraph Futomaki[Futomaki Combo 🍣 Big Data]
    neo4j([Neo4j]) --> weaviate([Weaviate])
    weaviate --> chroma([Chroma])
    chroma --> infinity([Infinity])
  end

  subgraph Nigiri[Nigiri Combo 🍤 AI/ML Specialties]
    litellm([LiteLLM]) --> whisper([Whisper])
    whisper --> piper([Piper])
    piper --> comfyui([ComfyUI])
  end

  subgraph Side[🍵 Side Dishes]
    rclone([Rclone]) --> jupyterlab([JupyterLab])
    jupyterlab --> vscode([VSCode Server])
    vscode --> homepage([Homepage])
  end

  subgraph Condiments[🌿 Condiments & Consoles]
    minioC([MinIO Console]) --> qdrantC([Qdrant Console])
    qdrantC --> neo4jB([Neo4j Browser])
    neo4jB --> doctor([Sushi Doctor])
  end

  subgraph Observability[📊 Observability Combo]
    prometheus([Prometheus]) --> grafana([Grafana])
    grafana --> cadvisor([cAdvisor])
    cadvisor --> nodeexporter([Node Exporter])
    grafana --> langfuse([Langfuse])
    langfuse --> loki([Loki-Promtail])
  end

  subgraph Security[🔒 Security Combo]
    authentik([Authentik]) --> caddy([Caddy Forward Auth])
    caddy --> infisical([Infisical])
    infisical --> vault([Vault])
  end

  subgraph Backups[💾 Backups Combo]
    borgmatic([Borgmatic]) --> pgbackrest([pgBackRest])
    pgbackrest --> neo4jbackup([Neo4j Admin Backup])
  end
