<p align="center">
  <img src="././assets/sushi kitchen 4.png" alt="Sushi Kitchen Banner" width="600"/>
</p>

# 🍣 Sushi Kitchen

Welcome to **Sushi Kitchen** — a composable, self-hosted AI development environment.  
Think of it like a sushi restaurant menu: pick your **Plate** (hardware size),  
choose a **Teishoku (Platter / Main Course)**, then add optional **rolls, soups,  
noodles, appetizers, or sides** to taste.

---

## 🥢 How to Order

### 1. Choose your Plate
Not sure how much sushi your computer can handle?  
See our [Hardware Sizing Guide](docs/plates.md) to pick the right Plate.

---

### 2. Pick your Main Course (Teishoku / Platters)

Each Teishoku is a **pre-assembled combo** of rolls (apps) that already work together.

#### Hosomaki Platter (Core)
- [**n8n**](docs/rolls/n8n.md) — automation and orchestration workflows  
- [**Supabase**](docs/rolls/supabase.md) — database + authentication platform  
- [**Postgres + pgvector**](docs/rolls/postgres.md) — relational DB with vector search  
- [**Qdrant (optional)**](docs/rolls/qdrant.md) — vector database alternative  
- [**Redis**](docs/rolls/redis.md) — caching and queues  
- [**LiteLLM**](docs/rolls/litellm.md) — unified LLM API router  
- [**Ollama (small)**](docs/rolls/ollama.md) — local LLM runner  
- [**MinIO**](docs/rolls/minio.md) — S3-compatible object storage  

#### Futomaki Platter (Knowledge & RAG)
- [**Neo4j**](docs/rolls/neo4j.md) — graph database  
- [**Weaviate (optional)**](docs/rolls/weaviate.md) — vector DB with modular extensions  
- [**Chroma (optional)**](docs/rolls/chroma.md) — simple vector DB  
- [**Infinity embeddings (optional)**](docs/rolls/infinity.md) — fast embedding service  

#### Temaki Platter (Voice & Interaction)
- [**Whisper**](docs/rolls/whisper.md) — speech-to-text  
- [**Piper**](docs/rolls/piper.md) — text-to-speech  

#### Uramaki Platter (Imaging)
- [**ComfyUI**](docs/rolls/comfyui.md) — image pipeline builder  
- [**rclone**](docs/rolls/rclone.md) — sync images to MinIO/S3  

#### Chirashi Platter (Data Science)
- [**JupyterLab**](docs/rolls/jupyterlab.md) — interactive notebooks  

#### Tamago Platter (Dev Tools)
- [**VS Code Server**](docs/rolls/vscode-server.md) — browser-based IDE  

---

<p align="left">
  <img src="././assets/sushi kitchen final.png" alt="Sushi Kitchen Banner" width="400" height="400"/>
</p>

### 3. Add Starters (Optional Dishes)

Still hungry? Round out your platter with extra dishes:

#### 🥟 Zensai (Appetizers)
- [**Homepage**](docs/rolls/homepage.md) — simple launchpad linking to all running UIs  
- [**MinIO Console**](docs/rolls/minio-console.md) — web console for object storage  
- [**Qdrant Console**](docs/rolls/qdrant-console.md) — UI for exploring vector collections  
- [**Neo4j Browser**](docs/rolls/neo4j-browser.md) — interactive graph explorer  
- [**sushi-doctor**](docs/rolls/sushi-doctor.md) — local helper script to check Docker, env, ports  

#### 🍲 Ramen (Observability & Health)
- [**Prometheus**](docs/rolls/prometheus.md) — metrics collection  
- [**Grafana**](docs/rolls/grafana.md) — dashboards & visualization  
- [**cAdvisor**](docs/rolls/cadvisor.md) — container resource monitoring  
- [**Node Exporter**](docs/rolls/node-exporter.md) — system metrics exporter  
- [**Langfuse (optional)**](docs/rolls/langfuse.md) — LLM trace observability  
- [**Loki + Promtail (enterprise)**](docs/rolls/loki-promtail.md) — centralized logging stack  

#### 🍜 Udon (Hearty Dev Tools)
- [**JupyterLab**](docs/rolls/jupyterlab.md) — notebooks for data science (also part of Chirashi Platter)  
- [**VS Code Server**](docs/rolls/vscode-server.md) — web IDE (also part of Tamago Platter)  

#### 🍱 Sides (Ops & Security Rails)
- **Hanko — Identity**:  
  - [**Authentik**](docs/rolls/authentik.md) — authentication and identity management  
  - [**Caddy forward-auth**](docs/rolls/caddy-forward-auth.md) — proxy-level auth integration  
- **Shio — Secrets**:  
  - [**Infisical**](docs/rolls/infisical.md) — lightweight secret management  
  - [**Vault OSS (optional)**](docs/rolls/vault.md) — enterprise-grade secret storage  
- **Tsukemono — Backups**:  
  - [**Borgmatic**](docs/rolls/borgmatic.md) — automated backups  
  - [**pgBackRest / wal-g**](docs/rolls/pgbackrest.md) — Postgres backup tools  
  - [**neo4j-admin backup**](docs/rolls/neo4j-admin-backup.md) — backup/restore graph data  

---

### 4. Enterprise? Order the Omakase
For enterprise customers: curated deployments, full support, and custom sizing.  
Omakase = we serve you directly.

---

## 🚀 Quick Start

```bash
git clone https://github.com/binarylawyer/sushi-kitchen.git
cd sushi-kitchen
./scripts/sushi-start.sh hosomaki
