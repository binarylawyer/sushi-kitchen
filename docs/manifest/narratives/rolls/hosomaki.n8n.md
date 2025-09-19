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
