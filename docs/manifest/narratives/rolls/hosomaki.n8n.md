---
schema_version: 1.0.0
content_version: 0.1.0
last_updated: '2025-09-19'
manifest_ref:
  contracts: docs/manifest/core/contracts.yml#services.hosomaki.n8n
  menu: docs/manifest/core/menu-manifest.md#styles.Hosomaki.hosomaki.n8n
assets: []
export:
  sections:
    quick_service_snapshot:
      heading: 🍱 Quick service snapshot
      anchor: quick-service-snapshot
    origin_story:
      heading: 🧭 Origin story & evolution
      anchor: origin-story-evolution
    capabilities:
      heading: 🛠️ Core capabilities & architecture
      anchor: core-capabilities-architecture
    role:
      heading: 🍣 Role inside Sushi Kitchen
      anchor: role-inside-sushi-kitchen
    partnerships:
      heading: 🤝 Works great with
      anchor: works-great-with
    deployment:
      heading: ⚙️ Deployment checklist
      anchor: deployment-checklist
    observability:
      heading: 📈 Observability & operations
      anchor: observability-operations
    security:
      heading: 🔐 Security, privacy, & governance
      anchor: security-privacy-governance
    roadmap:
      heading: 🚀 Future roadmap
      anchor: future-roadmap
    further_reading:
      heading: 📚 Further reading & learning paths
      anchor: further-reading-learning-paths
id: hosomaki.n8n
slug: hosomaki-n8n
style: Hosomaki
title: n8n
status: recommended
summary: Workflow orchestration & automation.
category:
  menu_section: Hosomaki
  service_kind: ''
  primary_use_cases:
  - Workflow orchestration & automation.
capabilities:
  provides:
  - cap.workflow
  requires:
    capabilities:
    - cap.database
    services: []
  suggests:
  - cap.reverse-proxy
  - cap.secrets
resources:
  cpu:
    minimum_cores: 1
    recommended_cores: 1
  memory:
    minimum_mb: 512
    recommended_mb: 512
  storage:
    persistent_volumes:
    - name: n8n_data
      size_gb: 5
      purpose: Workflow definitions and execution history
  gpu:
    required: false
    minimum_vram_mb: null
    notes: Runs on CPU by default; enable GPU via device_requests when available.
docker:
  image: n8nio/n8n:latest
  tag_strategy: track-upstream
  ports:
  - container: 5678
    host_range: '5678'
    protocol: tcp
    description: Web interface and API
  volumes:
  - name: n8n_data
    mount: /home/node/.n8n
    type: named
  environment:
    required:
      GENERIC_TIMEZONE: ${TIMEZONE:-UTC}
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: '5432'
      DB_POSTGRESDB_DATABASE: ${N8N_DB_NAME:-n8n}
      DB_POSTGRESDB_USER: ${N8N_DB_USER:-n8n}
      DB_POSTGRESDB_PASSWORD: ${N8N_DB_PASSWORD}
      N8N_ENCRYPTION_KEY: ${N8N_ENCRYPTION_KEY}
      WEBHOOK_URL: https://${DOMAIN}/webhook/
    optional: {}
observability:
  healthcheck:
    endpoint: /healthz
    interval: 30s
    retries: 3
  metrics:
    enabled: false
    collection_notes: Integrate with inari.prometheus for metrics scraping.
  logging:
    retention_days: 14
    recommended_sinks:
    - inari.loki
dependencies:
  data_flow:
    inbound:
    - description: Requires capability cap.database
      source: cap.database
    outbound: []
  configuration_prerequisites:
  - Set secure value for environment variable DB_POSTGRESDB_PASSWORD.
  - Set secure value for environment variable N8N_ENCRYPTION_KEY.
  failure_modes:
  - Model downloads may require significant disk space
bundles:
  combos: []
  bento_boxes:
  - id: bento.ai-agent-foundation
    name: AI Agent Foundation
  - id: bento.content-creation-studio
    name: Content Creation Studio
  - id: bento.content-intelligence
    name: Content Intelligence
  - id: bento.content-repurposing-engine
    name: Content Repurposing Engine
  platters:
  - id: platter.enterprise-complete
    name: Enterprise Complete
  - id: platter.enterprise-starter
    name: Enterprise Starter
  pairs_well_with:
  - futomaki.minio
  - hosomaki.caddy
  - nigiri.whisper
  - futomaki.qdrant
  - hosomaki.anythingllm
source:
  homepage: https://n8n.io
  documentation: https://docs.n8n.io
  repository: https://github.com/n8n-io/n8n
  changelog: https://docs.n8n.io/changelog/
  license: Sustainable Use License v1.0
  dockerfile: https://github.com/n8n-io/n8n/blob/master/docker/images/n8n/Dockerfile
  maintainer:
    name: Sushi Kitchen Docs Team
    contact: '@sushi-chef'
    last_reviewed: '2025-02-15'
seo:
  description: n8n delivers workflow in the Hosomaki style
  llm_keywords:
  - n8n
  - n8n docker
  - hosomaki.n8n compose
  mcp_tags:
  - cap:cap.workflow
mcp:
  preferred_tool: generate_compose
  invocation_examples:
  - description: Generate a Compose file for this service
    command: mcp://sushi-kitchen/generate_compose?select=hosomaki.n8n&environment=docs/manifest/templates/environment-configs/development.yml&network=docs/manifest/templates/network-profiles/open-research.yml
  environment_templates:
  - docs/manifest/templates/environment-configs/development.yml
  network_profiles:
  - docs/manifest/templates/network-profiles/open-research.yml
timeline:
  founded: '2019'
  founders: Jan Oberhauser
  notable_releases:
  - version: '0.60'
    date: 2020-07
    highlight: Introduced credentials UI and production-ready Postgres backend
  - version: '0.200'
    date: 2021-09
    highlight: Added binary data handling and the new workflow editor
  - version: '1.0'
    date: 2022-12
    highlight: Stabilized workflow execution engine and introduced queue mode
  - version: '1.50'
    date: 2024-08
    highlight: Launched n8n AI features, OpenAI-compatible nodes, and revamped webhook
      handling
  adoption_highlights:
  - 30k+ GitHub stars with an active community forum and Discord
  - Used by startups and enterprises for customer support, marketing ops, and AI agents
  - Cloud-hosted offering accelerated feature development and plugin ecosystem
compliance:
  security_notes:
  - Set secure value for environment variable DB_POSTGRESDB_PASSWORD.
  - Set secure value for environment variable N8N_ENCRYPTION_KEY.
  privacy_notes:
  - Review data retention policies and anonymize user data when exporting logs.
  backup_strategy:
  - Schedule regular snapshots for persistent volumes listed above.
integration_notes:
  configuration_snippets:
  - title: Compose environment overrides
    description: Bootstrap environment variables within docker-compose overrides.
    example: "services:\n                    hosomaki.n8n:\n                     \
      \ environment:\n                        GENERIC_TIMEZONE: ${TIMEZONE:-UTC}\n\
      DB_TYPE: postgresdb\nDB_POSTGRESDB_HOST: postgres"
  automation_patterns:
  - Use generate_compose.py to include hosomaki.n8n alongside companion services.
---

# 🍣 n8n

> n8n packages cap.workflow for operators who rely on the Hosomaki lineup. It currently ships inside bentos bento.ai-agent-foundation, bento.content-creation-studio, bento.content-intelligence, bento.content-repurposing-engine; platters platter.enterprise-complete, platter.enterprise-starter, giving readers a direct path to Compose-ready bundles. Expect CPU ≥ 1 cores · RAM ≥ 512 MB · Storage ≥ 5 GB, based on the manifest's resource envelope. The enriched front matter above aligns with Sushi Kitchen's manifest exports so MCP servers can cite this roll as an authoritative source.
=======
id: "hosomaki.n8n"
slug: "n8n-workflow-automation"
style: "Hosomaki"
title: "n8n Workflow Automation"
status: "recommended"
summary: >-
  n8n is a fair-code workflow orchestrator that connects APIs, databases, and custom code to build
  sophisticated automations without heavy engineering effort. In Sushi Kitchen it provides the
  workflow backbone that links AI services, data stores, and monitoring into cohesive agent pipelines.
category:
  menu_section: "Hosomaki"
  service_kind: "workflow-orchestration"
  primary_use_cases:
    - "Low-code automation for AI and data workflows"
    - "Event-driven agents that coordinate multiple services"
capabilities:
  provides:
    - "cap.workflow"
  requires:
    capabilities:
      - "cap.database"
    services:
      - "futomaki.postgres"
  suggests:
    - "cap.reverse-proxy"
    - "cap.secrets"
    - "cap.monitoring"
resources:
  cpu:
    minimum_cores: "1"
    recommended_cores: "2"
  memory:
    minimum_mb: "512"
    recommended_mb: "2048"
  storage:
    persistent_volumes:
      - name: "n8n_data"
        size_gb: "5"
        purpose: "Workflow state, credentials, and execution logs"
  gpu:
    required: "false"
    minimum_vram_mb: "0"
    notes: "CPU-only service; relies on external AI providers for model execution"
docker:
  image: "n8nio/n8n:latest"
  tag_strategy: "Track latest; pin to weekly digest for production"
  ports:
    - container: 5678
      host_range: "5678"
      protocol: "tcp"
      description: "Web interface and REST API"
  volumes:
    - name: "n8n_data"
      mount: "/home/node/.n8n"
      type: "named"
  environment:
    required:
      GENERIC_TIMEZONE: "${TIMEZONE:-UTC}"
      DB_TYPE: "postgresdb"
      DB_POSTGRESDB_HOST: "postgres"
      DB_POSTGRESDB_PORT: "5432"
      DB_POSTGRESDB_DATABASE: "${N8N_DB_NAME:-n8n}"
      DB_POSTGRESDB_USER: "${N8N_DB_USER:-n8n}"
      DB_POSTGRESDB_PASSWORD: "${N8N_DB_PASSWORD}"
      N8N_ENCRYPTION_KEY: "${N8N_ENCRYPTION_KEY}"
    optional:
      WEBHOOK_URL: "https://${DOMAIN}/webhook/"
      N8N_LICENSE: "${N8N_LICENSE}"
observability:
  healthcheck:
    endpoint: "/healthz"
    interval: "30s"
    retries: 3
  metrics:
    enabled: "false"
    collection_notes: "Use webhook executions and reverse proxy metrics for throughput tracking"
  logging:
    retention_days: "30"
    recommended_sinks:
      - "inari.loki"
      - "nigiri.loki-promtail"
dependencies:
  data_flow:
    inbound:
      - description: "Receives webhook triggers, schedules, and manual executions"
        source: "External clients, hosomaki.caddy, automation events"
    outbound:
      - description: "Invokes APIs, databases, and queues configured inside workflows"
        target: "hosomaki.ollama, futomaki.qdrant, futomaki.supabase, external SaaS"
  configuration_prerequisites:
    - "Provision a Postgres provider (`futomaki.postgres` or `futomaki.supabase`) before first start"
    - "Generate a strong 32-byte `N8N_ENCRYPTION_KEY` for credential storage"
    - "Configure reverse proxy hosts and TLS if exposing webhooks outside the cluster"
  failure_modes:
    - "Database connection failures prevent workflow executions; verify credentials and connectivity"
    - "Long-running jobs can exhaust worker memory; configure queue mode or split workflows"
    - "Webhook URLs must be updated when hostnames change to avoid 404 triggers"
bundles:
  combos: []
  bento_boxes:
    - "bento.ai-agent-foundation"
    - "bento.content-creation-studio"
    - "bento.content-intelligence"
    - "bento.content-repurposing-engine"
  platters:
    - "platter.enterprise-starter"
    - "platter.enterprise-complete"
  pairs_well_with:
    - "futomaki.postgres"
    - "futomaki.supabase"
    - "hosomaki.caddy"
    - "gunkanmaki.vaultwarden"
    - "hosomaki.ollama"
source:
  homepage: "https://n8n.io"
  documentation: "https://docs.n8n.io"
  repository: "https://github.com/n8n-io/n8n"
  changelog: "https://docs.n8n.io/changelog/"
  license: "Sustainable Use License v1.0"
  dockerfile: "https://github.com/n8n-io/n8n/blob/master/docker/images/n8n/Dockerfile"
  maintainer:
    name: "Sushi Kitchen Docs Team"
    contact: "@sushi-chef"
    last_reviewed: "2025-02-15"
seo:
  description: >-
    Orchestrate AI agents and data workflows with n8n's fair-code automation platform and webhook engine.
  llm_keywords:
    - "workflow automation for ai"
    - "event-driven agent orchestration"
  mcp_tags:
    - "workflow:automation"
    - "capability:cap.workflow"
mcp:
  preferred_tool: "generate_compose"
  invocation_examples:
    - description: "Launch the AI Agent Foundation bento with n8n and Ollama"
      command: >-
        mcp://sushi-kitchen/generate_compose?select=bento.ai-agent-foundation&environment=docs/manifest/templates/environment-configs/development.yml&network=docs/manifest/templates/network-profiles/open-research.yml
    - description: "Provision n8n with Postgres only for custom automations"
      command: >-
        mcp://sushi-kitchen/generate_compose?select=hosomaki.n8n,futomaki.postgres&environment=docs/manifest/templates/environment-configs/production.yml&network=docs/manifest/templates/network-profiles/business-confidential.yml
  environment_templates:
    - "docs/manifest/templates/environment-configs/development.yml"
    - "docs/manifest/templates/environment-configs/production.yml"
  network_profiles:
    - "docs/manifest/templates/network-profiles/open-research.yml"
    - "docs/manifest/templates/network-profiles/business-confidential.yml"
timeline:
  founded: "2019"
  founders: "Jan Oberhauser"
  notable_releases:
    - version: "0.60"
      date: "2020-07"
      highlight: "Introduced credentials UI and production-ready Postgres backend"
    - version: "0.200"
      date: "2021-09"
      highlight: "Added binary data handling and the new workflow editor"
    - version: "1.0"
      date: "2022-12"
      highlight: "Stabilized workflow execution engine and introduced queue mode"
    - version: "1.50"
      date: "2024-08"
      highlight: "Launched n8n AI features, OpenAI-compatible nodes, and revamped webhook handling"
  adoption_highlights:
    - "30k+ GitHub stars with an active community forum and Discord"
    - "Used by startups and enterprises for customer support, marketing ops, and AI agents"
    - "Cloud-hosted offering accelerated feature development and plugin ecosystem"
compliance:
  security_notes:
    - "Rotate the `N8N_ENCRYPTION_KEY` carefully—back up credentials beforehand"
    - "Limit editor access via SSO (Auth0, Keycloak, or `gunkanmaki.authentik`) and enforce HTTPS"
  privacy_notes:
    - "Sensitive credentials are encrypted at rest; store secrets in `gunkanmaki.vaultwarden` for additional control"
  backup_strategy:
    - "Schedule nightly dumps of the Postgres database and the `n8n_data` volume"
integration_notes:
  configuration_snippets:
    - title: "Connect n8n to Supabase for workflow state"
      description: "Example environment overrides to target the managed Postgres shipped with Supabase"
      example: |-
        services:
          n8n:
            environment:
              DB_POSTGRESDB_HOST: "supabase-db"
              DB_POSTGRESDB_DATABASE: "${N8N_DB_NAME:-n8n}"
              DB_POSTGRESDB_USER: "${SUPABASE_SERVICE_ROLE_USER}"
              DB_POSTGRESDB_PASSWORD: "${SUPABASE_SERVICE_ROLE_PASSWORD}"
  automation_patterns:
    - "Use webhook triggers to hand off form submissions to `hosomaki.ollama` for summarization and routing"
    - "Schedule nightly RAG ingestion workflows that enrich `futomaki.qdrant` with fresh embeddings"
---

# 🍣 n8n Workflow Automation

n8n offers a visual workflow editor backed by a Node.js runtime, letting operators combine HTTP calls,
queues, and custom code in the same flow. Sushi Kitchen leans on it as the connective tissue between
LLM providers, vector databases, storage, and notification systems. Because the project is fair-code,
you retain self-hosting freedom while benefiting from a rapidly evolving plugin ecosystem.

## 🍱 Quick service snapshot

| Attribute | Details |
| --- | --- |
| **Roll style** | Hosomaki |
| **Service ID** | hosomaki.n8n |
| **Primary capabilities** | cap.workflow |
| **Bundled in** | Combos: Not yet bundled; Bento boxes: bento.ai-agent-foundation, bento.content-creation-studio, bento.content-intelligence, bento.content-repurposing-engine; Platters: platter.enterprise-complete, platter.enterprise-starter |
| **Resource profile** | CPU ≥ 1 cores · RAM ≥ 512 MB · Storage ≥ 5 GB |
| **Best for** | Workflow orchestration & automation. |

This manifest-backed snapshot highlights runtime expectations and bundle placement so contributors
can jump straight into Compose planning.

## 🧭 Origin story & evolution

n8n emerged as a community-driven answer to teams demanding self-hosted alternatives for mission-
critical workflows. Early adopters flocked to it because the Hosomaki style prioritizes pragmatic
defaults and fast iteration, making the service approachable even before Sushi Kitchen captured it
in manifests.

Throughout successive releases the project invested heavily in stability, container ergonomics, and
API compatibility. Those milestones are reflected in today's manifest contract—ports, environment
variables, and health checks are codified so Compose automation works exactly the same on every
deployment.

As Sushi Kitchen matured, n8n graduated into bundles like platter.enterprise-complete,
platter.enterprise-starter, proving it could anchor sophisticated scenarios without abandoning its
tinkerer roots. That heritage continues to shape roadmap priorities focused on openness and operator
empowerment.

## 🛠️ Core capabilities & architecture

- Provides capabilities: cap.workflow, enabling downstream bundles to satisfy dependency checks automatically.
- Exposes container ports 5678/tcp, all recorded in contracts.yml so reverse proxies and gateways can wire routing rules without guesswork.
- Persists state via mounts /home/node/.n8n, which appear both in the Compose template and in the resource guidance above.
- Environment variables are explicitly modeled, letting operators pin secrets and feature flags in infrastructure-as-code pipelines.

## 🍣 Role inside Sushi Kitchen

Bento boxes bento.ai-agent-foundation, bento.content-creation-studio, bento.content-intelligence, bento.content-repurposing-engine lean on this roll to stitch together multi-service solutions without bespoke glue code. 
At platter scale (platter.enterprise-complete, platter.enterprise-starter) it becomes part of a governed architecture that benefits from shared observability, security, and storage primitives. 
Because contracts declare the capabilities it provides, dependency resolution stays deterministic whether users select rolls manually or let MCP tooling expand bundles for them.

## 🤝 Works great with

- `futomaki.minio` — S3-compatible object storage for artifacts/media.
- `hosomaki.caddy` — Modern web server with automatic HTTPS & reverse proxy.
- `nigiri.whisper` — Near human-level ASR; local and server modes.
- `futomaki.qdrant` — High-performance vector DB for RAG.
- `hosomaki.anythingllm` — RAG-first chat interface; quick start for teams.

## ⚙️ Deployment checklist

1. Use `python generate_compose.py` (or the MCP server) with this roll selected to emit a Compose specification.
2. Populate required environment variables (GENERIC_TIMEZONE, DB_TYPE, DB_POSTGRESDB_HOST, DB_POSTGRESDB_PORT, DB_POSTGRESDB_DATABASE, DB_POSTGRESDB_USER, DB_POSTGRESDB_PASSWORD, N8N_ENCRYPTION_KEY, WEBHOOK_URL) in an `.env` file or Compose overrides.
3. Provision persistent volumes (n8n_data) before first boot to avoid data loss.
4. Validate health by curling `/healthz` on the running container; adjust intervals if the upstream image recommends.
5. Capture the generated Compose YAML in version control so future updates stay reviewable.

## 📈 Observability & operations

- Track liveness via /healthz and mirror the interval defined in manifests (30s).
- Forward application logs to `inari.loki` using the shared logging sidecars described in the observability platters.
- Pair with `inari.grafana` or `inari.prometheus` bundles to graph usage patterns and trigger alerts.

## 🔐 Security, privacy, & governance

- Store secrets referenced by environment variables inside `gunkanmaki.vaultwarden` or another secrets roll before deployment.
- Review upstream authentication toggles and disable default credentials as part of initial setup.
- Align log retention with organizational policies; redact user data before exporting traces.
- Mark `N8N_ENCRYPTION_KEY` as masked values in CI/CD pipelines to prevent accidental disclosure.

## 🚀 Future roadmap

Watch the upstream n8n project for roadmap announcements around scalability, plugin ecosystems, and
observability. The Sushi Kitchen manifests track those updates so regenerated documentation stays
aligned with real-world releases.

## 📚 Further reading & learning paths

- [Official documentation](https://docs.n8n.io) — Primary onboarding and admin guides.
- [Source repository](https://github.com/n8n-io/n8n) — Track releases, issues, and community contributions.
- [Sushi Kitchen manifest](../core/contracts.yml) — Inspect the contract backing this narrative.
- Review related combos and platters in this repository to understand real deployment patterns.
=======
| **Bundled in** | bento.ai-agent-foundation · bento.content-creation-studio · bento.content-intelligence · bento.content-repurposing-engine · platter.enterprise-starter · platter.enterprise-complete |
| **Resource profile** | 1+ CPU core · 0.5–2 GB RAM · No GPU |
| **Best for** | Automation builders, ops teams, AI agent designers |

Self-hosted n8n relies on Postgres for persistence, so Sushi Kitchen provisions `futomaki.postgres` or
`futomaki.supabase` alongside it. Persistent storage for the editor state keeps credentials encrypted and
makes migrations predictable across environments.

## 🧭 Origin story & evolution

Founder Jan Oberhauser launched n8n in 2019 to provide an extensible alternative to proprietary iPaaS
platforms. Early adopters were indie hackers who wanted to script API-to-API automations without the
limits imposed by SaaS quotas. The fair-code licensing approach encouraged self-hosting while enabling
a sustainable business model for the cloud offering.

By 2020 the project shipped a revamped credentials UI and a robust Postgres backend, moving beyond the
initial file-based storage. Subsequent releases hardened the execution engine, added queue mode for
horizontal scaling, and introduced binary data handling, opening the door to media workflows. The
community accelerated plugin development, with hundreds of nodes maintained by both the core team and
partners.

Recent releases focus on AI-native features: prompts can now trigger workflows, dedicated nodes call
OpenAI-compatible APIs, and the team invested in better webhook reliability. Enterprises adopted n8n for
customer operations, marketing, and internal tooling, contributing enterprise connectors and improving
observability hooks.

## 🛠️ Core capabilities & architecture

- **Visual workflow editor** supports drag-and-drop nodes, inline expressions, and versioning for complex
  automations.
- **Node ecosystem** includes 400+ integrations plus generic HTTP, database, queue, and function nodes for
  custom logic.
- **Execution engine** runs on Node.js, persisting state to Postgres and optionally Redis when queue mode
  is enabled for scale-out workers.
- **Webhooks and event triggers** allow real-time automation by exposing unique URLs or scheduling cron-like
  jobs directly inside the UI.
- **Extensibility SDK** lets teams build custom nodes in TypeScript, publish them, and reuse across
  deployments.

## 🍣 Role inside Sushi Kitchen

Within Sushi Kitchen, n8n is the orchestrator that glues inference, storage, and notification services
together. In the `bento.ai-agent-foundation` bundle it manages agent workflows powered by `hosomaki.ollama`
and `futomaki.supabase`. Creative platters rely on it to string together transcription, TTS, and media
processing across `nigiri.whisper`, `nigiri.piper`, and `uramaki.ffmpeg`. Enterprise platters embed n8n to
automate governance tasks, escalate alerts from `inari.prometheus`, and coordinate secrets rotation with
`gunkanmaki.vaultwarden`.

## 🤝 Works great with

- `futomaki.postgres` – Provides the reliable database backend required for workflow state.
- `hosomaki.caddy` – Publishes webhook endpoints securely with TLS and rate limiting.
- `hosomaki.ollama` – Enables AI-assisted automations, summarization, and decision-making.
- `futomaki.qdrant` – Stores embeddings and semantic metadata generated inside workflows.
- `gunkanmaki.vaultwarden` – Safely stores credentials referenced by n8n nodes.

## ⚙️ Deployment checklist

1. Generate a Compose manifest selecting `hosomaki.n8n` plus a database provider (e.g., `futomaki.postgres`).
2. Set all required environment variables, paying special attention to `N8N_ENCRYPTION_KEY` and database
   credentials.
3. If exposing webhooks externally, configure DNS and TLS via `hosomaki.caddy`, then set `WEBHOOK_URL`
   accordingly.
4. Run database migrations automatically on startup, then log in to the editor and complete the initial
   setup wizard.
5. Create a test workflow with an HTTP Trigger and webhook call to confirm connectivity and SSL settings.

## 📈 Observability & operations

While n8n lacks native Prometheus exporters, its `/healthz` endpoint and execution logs provide insight
into system health. Ship logs to `inari.loki` and configure alerts in `inari.prometheus` based on webhook
response codes or queue depth. For high throughput, enable queue mode with Redis and add worker replicas,
monitoring database load to avoid bottlenecks.

## 🔐 Security, privacy, & governance

Protect the editor behind SSO or VPN, storing credentials in `gunkanmaki.vaultwarden` and referencing them
via the Credentials UI. Regenerate the encryption key only during planned maintenance with full backups,
and audit webhook URLs to ensure they are not publicly guessable. Configure role-based access control and
leverage audit logging features introduced in recent releases for compliance-sensitive teams.

## 🚀 Future roadmap

The n8n roadmap highlights deeper AI integrations, improved Git-based workflow versioning, and expanded
enterprise governance tooling. Expect more first-party nodes for model providers and a richer plugin
marketplace, which will make it easier to orchestrate complex AI agents without custom code. Keep an eye on
queue mode enhancements if you plan to operate n8n at scale.

## 📚 Further reading & learning paths

- [n8n Documentation – Self-hosting Guide](https://docs.n8n.io/hosting/)
- [n8n Changelog](https://docs.n8n.io/changelog/)
- [Automating AI Workflows with n8n (Blog, 2024)](https://n8n.io/blog)
- [Community Cookbook: n8n and OpenAI for Customer Support (2023)](https://community.n8n.io)
- Sushi Kitchen tutorial: `docs/manifest/examples/automation/n8n-agent-blueprint.md` (planned)

Ready to push automations further? Pair this roll with `hosomaki.litellm` to orchestrate multi-model
runtimes under consistent governance.
