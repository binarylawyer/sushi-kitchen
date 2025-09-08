title: Gitea
profile: tamago
category: devtools
status: optional
image: gitea/gitea:latest
ports: ["3350:3000", "3351:22"]
env_vars:
USER_UID: "1000" # UID for the git user inside the container
USER_GID: "1000" # GID for the git user inside the container
GITEA__database__DB_TYPE: "sqlite3" # Database type (sqlite3 by default)
GITEA__database__HOST: "" # External DB host (if using MySQL/Postgres)
GITEA__database__NAME: "gitea" # Database name when using an external DB
GITEA__database__USER: "gitea" # DB user for external DB
GITEA__database__PASSWD: "gitea" # DB password for external DB
requires: []
resources:
cpu: "0.5-1"
ram: "512MB"
gpu: false
otel:
service_name: "gitea"
exporters: ["otlp"]
loki:
labels: ["app=gitea", "roll=tamago"]
security:
secrets: ["GITEA__security__SECRET_KEY", "GITEA__security__INTERNAL_TOKEN"]
sso: false
last_updated: 2025-09-08
maintainers: ["@binarylawyer"]
What it is

Gitea is a lightweight, self‑hosted Git service written in Go. It provides a full suite of Git hosting features, including code hosting, pull requests, issues, a built‑in container registry and package server, and a web‑based interface similar to GitHub or GitLab. Because it’s fully open source and easy to deploy, Gitea makes it simple to run your own private Git server with minimal resources.

Why you’d use it

To host private or internal Git repositories without relying on third‑party services.

To provide pull requests, code review, issue tracking and CI integrations in a self‑contained environment.

To run a lightweight Git service alongside your AI/ML stack without the overhead of GitLab.

To experiment with GitOps workflows locally before deploying them on cloud infrastructure.

Quick start

Launch Gitea using the Tamago profile:

docker compose --profile tamago up -d gitea


Access the web UI at http://localhost:3350
. During the initial setup wizard you can choose SQLite (default) or connect to an external database (MySQL/Postgres) using the GITEA__database__* environment variables.

If you need SSH access, the service listens on port 22 inside the container and is mapped to host port 3351. You can clone repositories via SSH after adding your public key in the web UI.

Configuration
Environment variables
Variable	Default	Required	Description
USER_UID	1000	Yes	The user ID that runs the Gitea process inside the container. Set this to match a host user if using bind mounts.
USER_GID	1000	Yes	The group ID for the Gitea process inside the container.
GITEA__database__DB_TYPE	sqlite3	No	Database backend (sqlite3, mysql, postgres). When using mysql or postgres, set the other GITEA__database__* variables.
GITEA__database__HOST	(empty)	No	Hostname and port of the external database, e.g. db:3306.
GITEA__database__NAME	gitea	No	Name of the database when using an external DB.
GITEA__database__USER	gitea	No	Database user for MySQL/Postgres.
GITEA__database__PASSWD	gitea	No	Database password for MySQL/Postgres.
GITEA__security__SECRET_KEY	(none)	Yes	Secret key for encrypting cookies and sessions. Generate with gitea generate secret SECRET_KEY.
GITEA__security__INTERNAL_TOKEN	(none)	Yes	Internal JWT token used by Gitea. Generate with gitea generate secret INTERNAL_TOKEN.
Volumes

Gitea stores repositories, configuration and data in /data. Mount a persistent volume to this path to retain your data:

volumes:
  - gitea_data:/data
  # optional: share host SSH keys if you are using container passthrough
  # - /home/git/.ssh/:/data/git/.ssh

Ports & exposure

Gitea exposes two ports:

The web UI listens on port 3000 inside the container. In our default deployment this is mapped to host port 3350 to avoid conflicts. If you prefer to run it on the standard 3000 port, change the host mapping to "3000:3000".

The SSH server listens on port 22 inside the container. It is mapped to host port 3351. You can change the host port to 2222 (as in the official docs) or any other free port.

If you use a reverse proxy like Caddy, you may map only the necessary ports and route via a subdomain instead of exposing these ports directly.

Compose snippet

Here is a minimal service definition for Gitea using SQLite. Add this to your docker-compose.yml:

services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    profiles: ["tamago"]
    ports:
      - "3350:3000"  # web UI
      - "3351:22"    # SSH
    environment:
      - USER_UID=${USER_UID:-1000}
      - USER_GID=${USER_GID:-1000}
      # Uncomment below to use MySQL or Postgres
      # - GITEA__database__DB_TYPE=mysql
      # - GITEA__database__HOST=db:3306
      # - GITEA__database__NAME=gitea
      # - GITEA__database__USER=gitea
      # - GITEA__database__PASSWD=gitea
      - GITEA__security__SECRET_KEY=${GITEA__security__SECRET_KEY}
      - GITEA__security__INTERNAL_TOKEN=${GITEA__security__INTERNAL_TOKEN}
    volumes:
      - gitea_data:/data
    restart: unless-stopped
    depends_on:
      - caddy

volumes:
  gitea_data:

Integrations

Database backends: For small teams, the default SQLite backend is sufficient. For larger setups, configure Gitea to use MySQL or Postgres and link to your existing database service (e.g. Supabase or a dedicated MySQL/Postgres container).

Authentik/OAuth: Gitea can integrate with external OAuth providers. If you run Authentik or Keycloak, set up an OAuth application in those services and configure Gitea accordingly in the app.ini under [oauth].

CI/CD: Gitea pairs well with Drone or Gitea Actions for continuous integration. You can use the Gitea API with n8n to automate repository hooks.

Observability: Enable OpenTelemetry exporter via otel settings to send traces to your observability stack (Prometheus/Grafana). Use the default Loki labels defined above to collect logs via Promtail.

Security notes

Secrets: Always generate fresh values for GITEA__security__SECRET_KEY and GITEA__security__INTERNAL_TOKEN using the gitea generate secret commands. Store these secrets in Infisical or Vaultwarden and inject them via environment variables.

User permissions: Avoid running the container as root. Set USER_UID and USER_GID to match the host user that owns the mounted volume. This prevents permission issues and improves security.

SSH exposure: If you don’t require SSH access, you can omit the port mapping for 22 entirely. When exposing SSH, consider binding it to 127.0.0.1 to restrict access to local or proxied connections.

TLS and Reverse Proxy: Place Gitea behind Caddy or another reverse proxy to enable HTTPS, path routing and automatic TLS certificates.

Troubleshooting

Permissions errors on startup: Ensure that the volume mounted at /data is writable by the UID/GID specified via USER_UID and USER_GID.

Unable to connect to external database: Verify that the GITEA__database__HOST, NAME, USER, and PASSWD variables are set correctly and that the database container is reachable from Gitea.

SSH authentication problems: Make sure the SSH port mapping is correct and that your SSH key is added to your Gitea account. If using host passthrough, follow the official docs to share /home/git/.ssh and match UID/GID between host and container.

References

Official documentation: Gitea – Installation with Docker

Gitea GitHub repository: https://github.com/go-gitea/gitea
