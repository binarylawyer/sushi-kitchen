# n8n

**What it is**  
n8n is a powerful workflow automation platform that connects your apps and services with a visual, node-based editor—like Zapier but self-hosted and with full code access when you need it.

<details>
<summary><strong>⚙️ Service Metadata</strong> <em>(click to expand)</em></summary>

```yaml
title: n8n
profile: hosomaki
category: automation
status: core
image: n8nio/n8n:1.23.0
ports: ["5678:5678"]
env_vars:
  N8N_ENCRYPTION_KEY: "${N8N_ENCRYPTION_KEY}"
  N8N_HOST: "${N8N_HOST:-localhost}"
  N8N_PORT: "5678"
  N8N_PROTOCOL: "${N8N_PROTOCOL:-http}"
  DB_TYPE: "postgresdb"
  DB_POSTGRESDB_HOST: "postgres"
  DB_POSTGRESDB_PORT: "5432"
  DB_POSTGRESDB_DATABASE: "${POSTGRES_DB:-sushidb}"
  DB_POSTGRESDB_USER: "${POSTGRES_USER:-sushi}"
  DB_POSTGRESDB_PASSWORD: "${POSTGRES_PASSWORD:-changeme}"
  EXECUTIONS_DATA_SAVE_ON_ERROR: "all"
  EXECUTIONS_DATA_SAVE_ON_SUCCESS: "all"
  GENERIC_TIMEZONE: "${TZ:-America/New_York}"
requires: [postgres, redis]
resources:
  cpu: "1-2"
  ram: "1GB-4GB"
  gpu: false
  storage: "5GB+"
otel:
  service_name: "n8n"
  exporters: ["otlp", "prometheus"]
loki:
  labels: ["app=n8n","roll=hosomaki"]
security:
  secrets: ["N8N_ENCRYPTION_KEY", "DB_PASSWORD"]
  sso: true
  auth_methods: ["basic", "oauth2", "api_key"]
last_updated: 2025-01-12
maintainers: ["@sushichef"]
```

</details>

---

## **Summary Table**

| **Field** | **Value** |
|-----------|-----------|
| **Title** | n8n |
| **Profile** | hosomaki |
| **Category** | automation |
| **Status** | core |
| **Image** | `n8nio/n8n:1.23.0` |
| **Ports** | `5678:5678` (Web UI & API) |
| **Resources** | CPU: 1-2 cores, RAM: 1-4GB, GPU: no |
| **OTEL** | service_name=`n8n`, exporters=`otlp, prometheus` |
| **Loki Labels** | `app=n8n`, `roll=hosomaki` |
| **Security** | Secrets: `N8N_ENCRYPTION_KEY`, SSO: yes |
| **Last Updated** | 2025-01-12 |
| **Maintainers** | @sushichef |

---

[Rest of content continues as before...]
