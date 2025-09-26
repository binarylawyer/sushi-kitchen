Install Guide

## Requirements
- OS: Ubuntu 22.04+/Debian 12+, macOS (Docker Desktop), Windows (WSL2)
- CPU: 4 vCPU / 8 GB RAM (Lite)
- Full: 8 vCPU / 16 GB RAM, optional NVIDIA GPU
- Disk: 20–40 GB free (models & logs)

## Steps
1. Install Docker & Compose plugin.
2. Clone repo and copy env:
   ```bash
   git clone https://github.com/<yourorg>/sushi-kitchen.git
   cd sushi-kitchen
   cp .env.example .env
   ./install/setup.sh
   ```
3. Start Lite profile
    ```bash
    docker compose --profile core up -d
    ```

or Full:
```bash
docker compose up -d
```

## GPU (NVIDIA)

Install NVIDIA drivers & nvidia-container-toolkit.
Recreate stack; Ollama will detect GPU automatically.

## Remote VPS

Open only necessary ports; prefer SSH tunnel access.

Phase 2: Caddy + Cloudflare Tunnel wizard for HTTPS & zero-trust.

## First Checks

n8n: http://<host>:5678
(Full) Grafana: http://<host>:13000
(Full) Langfuse: http://<host>:3005