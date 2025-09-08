---
title: Gitea
profile: tamago
category: devtools
status: optional
image: gitea/gitea:latest
ports: ["3350:3000", "3351:22"]
env_vars:
  USER_UID: "1000"
  USER_GID: "1000"
  GITEA_DB_TYPE: "sqlite3"
  GITEA_DB_HOST: ""
  GITEA_DB_NAME: ""
  GITEA_DB_USER: ""
  GITEA_DB_PASSWORD: ""
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
last_updated: 2025-09-08
maintainers: ["@binarylawyer"]
---

# **Gitea**

**What it is**  
Self-hosted Git service with a web UI, issues, pull requests, and CI hooks — a lightweight alternative to GitHub/GitLab.

---

## **Summary Table**

| **Field**       | **Value** |
|-----------------|-----------|
| **Title**       | Gitea |
| **Profile**     | tamago |
| **Category**    | devtools |
| **Status**      | optional |
| **Image**       | `gitea/gitea:latest` |
| **Ports**       | `3350:3000` (HTTP), `3351:22` (SSH) |
| **Resources**   | CPU: 1+, RAM: 512MB+, GPU: false |
| **OTEL**        | service_name=`gitea`, exporters=`otlp` |
| **Loki Labels** | `app=gitea`, `roll=tamago` |
| **Security**    | Secrets: `GITEA_DB_PASSWORD`, SSO: false |
| **Last Updated**| 2025-09-08 |
| **Maintainers** | @binarylawyer |

---

## **Why you’d use it**

* Host your own Git repositories privately inside Sushi Kitchen.  
* Lightweight, easy to run, simple backup/restore.  
* Integrates with n8n, CI/CD pipelines, and OAuth SSO.  

---

## **Quick start**

```bash
docker compose --profile tamago up -d gitea
```

- **Web UI:** http://localhost:3350  
- **SSH:** `ssh://git@localhost:3351`  
- **First run:** Set `ROOT_URL` to `http://localhost:3350/`.



# Configuration

### Environment Variables



| **Variable**        | **Default**              | **Required**      | **Notes**                          |
|---------------------|--------------------------|-------------------|------------------------------------|
| `USER_UID`          | `1000`                   | No                | UID for git user                   |
| `USER_GID`          | `1000`                   | No                | GID for git user                   |
| `GITEA_DB_TYPE`     | `sqlite3`                | Yes               | Options: `sqlite3`, `postgres`, `mysql` |
| `GITEA_DB_HOST`     | (empty)                  | If DB≠sqlite3     | Database host:port                 |
| `GITEA_DB_NAME`     | (empty)                  | If DB≠sqlite3     | Database name                      |
| `GITEA_DB_USER`     | (empty)                  | If DB≠sqlite3     | Database user                      |
| `GITEA_DB_PASSWORD` | (empty)                  | If DB≠sqlite3     | Database password (store securely) |
| `GITEA_ROOT_URL`    | `http://localhost:3350/` | Yes               | Public base URL                    |
| `GITEA_SSH_DOMAIN`  | `localhost`              | No                | Domain for SSH clone URLs          |
| `GITEA_SSH_PORT`    | `3351`                   | No                | Host SSH port for clone URLs       |

Volumes

gitea_data:/data — stores repositories, attachments, configs.

## **Compose snippet**

```yaml
services:
  gitea:
    image: gitea/gitea:latest
    profiles: ["tamago"]
    ports:
      - "3350:3000"  # HTTP
      - "3351:22"    # SSH
    environment:
      - USER_UID=${USER_UID:-1000}
      - USER_GID=${USER_GID:-1000}
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

```

---

## Integrations

n8n (webhooks & automations)

Authentik (SSO via OAuth)

Promtail + Loki (logs)

OTEL collector (traces)

## Security notes

Store GITEA_DB_PASSWORD in Infisical or Vaultwarden.

Consider putting Gitea behind Caddy/Authentik for TLS + SSO.

## Troubleshooting

Wrong clone URLs? → Set ROOT_URL properly.

SSH clone fails? → Verify host mapping 3351:22 and firewall rules.

## **References**

- [Gitea Docs](https://docs.gitea.com/)
- [Docker Hub — gitea/gitea](https://hub.docker.com/r/gitea/gitea)
