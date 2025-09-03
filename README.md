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
- **Supabase** — database + authentication platform  
- **Postgres + pgvector** — relational DB with vector search  
- **Qdrant (optional)** — vector database alternative  
- **Redis** — caching and queues  
- **LiteLLM** — unified LLM API router  
- **Ollama (small)** — local LLM runner  
- **MinIO** — S3-compatible object storage  

#### Futomaki Platter (Knowledge & RAG)
- **Neo4j** — graph database  
- **Weaviate (optional)** — vector DB with modular extensions  
- **Chroma (optional)** — simple vector DB  
- **Infinity embeddings (optional)** — fast embedding service  

#### Temaki Platter (Voice & Interaction)
- **Whisper** — speech-to-text  
- **Piper** — text-to-speech  

#### Uramaki Platter (Imaging)
- **ComfyUI** — image pipeline builder  
- **rclone** — sync images to MinIO/S3  

#### Chirashi Platter (Data Science)
- **JupyterLab** — interactive notebooks  

#### Tamago Platter (Dev Tools)
- **VS Code Server** — browser-based IDE  

---

<p align="left">
  <img src="././assets/sushi kitchen final.png" alt="Sushi Kitchen Banner" width="400" height="400"/>
</p>

### 3. Add Starters (Optional Dishes)

Still hungry? Round out your platter with extra dishes:

#### 🥟 Zensai (Appetizers)
- **Homepage** — simple launchpad linking to all running UIs  
- **MinIO Console** — web console for object storage  
- **Qdrant Console** — UI for exploring vector collections  
- **Neo4j Browser** — interactive graph explorer  
- **sushi-doctor** — local helper script to check Docker, env, ports  

#### 🍲 Soups (Observability & Health)
- **Prometheus** — metrics collection  
- **Grafana** — dashboards & visualization  
- **cAdvisor** — container resource monitoring  
- **Node Exporter** — system metrics exporter  
- **Langfuse (optional)** — LLM trace observability  
- **Loki + Promtail (enterprise)** — centralized logging stack  

#### 🍜 Noodles (Hearty Dev Tools)
- **JupyterLab** — notebooks for data science (also part of Chirashi Platter)  
- **VS Code Server** — web IDE (also part of Tamago Platter)  

#### 🍱 Sides (Ops & Security Rails)
- **Hanko — Identity**:  
  - **Authentik** — authentication and identity management  
  - **Caddy forward-auth** — proxy-level auth integration  
- **Shio — Secrets**:  
  - **Infisical** — lightweight secret management  
  - **Vault OSS (optional)** — enterprise-grade secret storage  
- **Tsukemono — Backups**:  
  - **Borgmatic** — automated backups  
  - **pgBackRest / wal-g** — Postgres backup tools  
  - **neo4j-admin backup** — backup/restore graph data  

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
