---
title: Gitea
profile: tamago
category: devtools
status: optional
image: gitea/gitea:latest
# keep container ports "normal" for compatibility; only the host side changes if needed
ports: ["3350:3000", "3351:22"]
env_vars:
  USER_UID: "1000"
  USER_GID: "1000"
  GITEA_DB_TYPE: "sqlite3"          # postgres | mysql | sqlite3
  GITEA_DB_HOST: ""                 # e.g., postgres:5432
  GITEA_DB_NAME: ""                 # e.g., gitea
  GITEA_DB_USER: ""                 # e.g., gitea
  GITEA_DB_PASSWORD: ""             # required if DB_TYPE != sqlite3
  GITEA_ROOT_URL: "http://localhost:3350/"
  GITEA_SSH_DOMAIN: "localhost"
  GITEA_SSH_PORT: "3351"
requires: []
resources:
  cpu: "1+"
  ram: "512MB+"
  gpu: false
otel:
  service_name: "gitea"
  exporters: ["otlp"]
loki:
  labels: ["app=gitea","roll=tamago"]
security:
  secrets: ["GITEA_DB_PASSWORD"]
  sso: false
last_updated: 2025-09-07
maintainers: ["@binarylawyer"]
---

**What it is**  
*Self-hosted Git service with web UI, issues, PRs, and CI hooks; lightweight GitHub/GitLab alternative.*

**Why you’d use it**  
* Host your code privately inside Sushi Kitchen.  
* Integrate with n8n or CI tools for build/deploy automations.  
* Works offline; simple backups via `/data`.

**Quick start**  
* `docker compose --profile tamago up -d gitea`  
* Web UI at: `http://localhost:3350` (container listens on `3000`)  
* SSH at: `ssh://git@localhost:3351` (container listens on `22`)  
* First-run: create admin user in the web UI; set **ROOT_URL** to `http://localhost:3350/`.

**Configuration**  
*Environment variables (common)*

| Variable              | Default                  | Required | Notes                                           |
|-----------------------|--------------------------|----------|-------------------------------------------------|
| `USER_UID`            | `1000`                   | No       | UID for `git` user                              |
| `USER_GID`            | `1000`                   | No       | GID for `git` user                              |
| `GITEA_DB_TYPE`       | `sqlite3`                | Yes      | `sqlite3`, `postgres`, or `mysql`               |
| `GITEA_DB_HOST`       | (empty)                  | If DB≠sqlite3 | e.g., `postgres:5432`                        |
| `GITEA_DB_NAME`       | (empty)                  | If DB≠sqlite3 | Database name                                 |
| `GITEA_DB_USER`       | (empty)                  | If DB≠sqlite3 | Database user                                 |
| `GITEA_DB_PASSWORD`   | (empty)                  | If DB≠sqlite3 | Database password (store in Infisical/Vault) |
| `GITEA_ROOT_URL`      | `http://localhost:3350/` | Yes      | Public base URL                                 |
| `GITEA_SSH_DOMAIN`    | `localhost`              | No       | Domain for SSH clone URLs                       |
| `GITEA_SSH_PORT`      | `3351`                   | No       | Host SSH port in clone URLs                     |

*Volumes*  
* `gitea_data:/data` — repositories, attachments, configs.

**Ports & volumes**  
* Container uses **3000** (HTTP) and **22** (SSH) to stay “normal.”  
* Default host mappings are **3350:3000** and **3351:22** to avoid clashes.  
* If your host’s 3000 is free, you can map to `3000:3000` instead.

**Compose snippet**
```yaml
services:
  gitea:
    image: gitea/gitea:latest
    profiles: ["tamago"]
    ports:
      - "3350:3000"    # HTTP  (container 3000)
      - "3351:22"      # SSH   (container 22)
    environment:
      - USER_UID=${GITEA_USER_UID:-1000}
      - USER_GID=${GITEA_USER_GID:-1000}
      - GITEA__database__DB_TYPE=${GITEA_DB_TYPE:-sqlite3}
      - GITEA__database__HOST=${GITEA_DB_HOST:-}
      - GITEA__database__NAME=${GITEA_DB_NAME:-}
      - GITEA__database__USER=${GITEA_DB_USER:-}
      - GITEA__database__PASSWD=${GITEA_DB_PASSWORD:-}
      - GITEA__server__ROOT_URL=${GITEA_ROOT_URL:-http://localhost:3350/}
      - GITEA__server__SSH_DOMAIN=${GITEA_SSH_DOMAIN:-localhost}
      - GITEA__server__SSH_PORT=${GITEA_SSH_PORT:-3351}
    volumes:
      - gitea_data:/data
    # depends_on:
    #   - caddy

Integrations

Works nicely with: n8n (webhooks), Authentik (SSO via OAuth), Promtail/Loki (logs), OTEL (traces).

Security notes

Store GITEA_DB_PASSWORD in Infisical/Vaultwarden.

Consider putting Gitea behind Caddy/Authentik for TLS/SSO.

Troubleshooting

If web UI returns wrong clone URLs, set ROOT_URL properly.

SSH clone issues: confirm host mapping 3351:22 and your firewall rules.

References

https://docs.gitea.com/

https://hub.docker.com/r/gitea/gitea
