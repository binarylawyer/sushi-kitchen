---
schema_version: 1.0.0
content_version: 0.1.0
last_updated: '2025-09-19'
manifest_ref:
  contracts: docs/manifest/core/contracts.yml#services.hosomaki.ollama
  menu: docs/manifest/core/menu-manifest.md#styles.Hosomaki.hosomaki.ollama
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
id: hosomaki.ollama
slug: hosomaki-ollama
style: Hosomaki
title: Ollama
status: recommended
summary: Local LLM engine with a huge community.
category:
  menu_section: Hosomaki
  service_kind: ''
  primary_use_cases:
  - Local LLM engine with a huge community.
  - chat
capabilities:
  provides:
  - cap.llm-api
  - cap.embeddings
  requires:
    capabilities: []
    services: []
  suggests: []
resources:
  cpu:
    minimum_cores: 2
    recommended_cores: 2
  memory:
    minimum_mb: 4096
    recommended_mb: 4096
  storage:
    persistent_volumes:
    - name: ollama_data
      size_gb: 50
      purpose: Model cache and runtime state
  gpu:
    required: true
    minimum_vram_mb: 8192
    notes: Requires NVIDIA GPUs with at least 8192 MB of VRAM.
docker:
  image: ollama/ollama:latest
  tag_strategy: track-upstream
  ports:
  - container: 11434
    host_range: '11434'
    protocol: tcp
    description: LLM inference API
  volumes:
  - name: ollama_data
    mount: /root/.ollama
    type: named
  environment:
    required:
      OLLAMA_HOST: 0.0.0.0
      OLLAMA_MODELS: /root/.ollama/models
      OLLAMA_KEEP_ALIVE: 24h
      CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-all}
    optional: {}
observability:
  healthcheck:
    endpoint: /api/tags
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
    inbound: []
    outbound: []
  configuration_prerequisites:
  - Review environment variable defaults before deployment.
  failure_modes:
  - Model downloads may require significant disk space
bundles:
  combos:
  - id: combo.chat-local
    name: Local Chat
  bento_boxes:
  - id: bento.ai-agent-foundation
    name: AI Agent Foundation
  platters:
  - id: platter.hosomaki-core
    name: Hosomaki Core
  - id: platter.omakase
    name: Omakase
  - id: platter.voice-first
    name: Voice First
  pairs_well_with:
  - nigiri.open-webui
  - hosomaki.litellm
  - hosomaki.caddy
  - chirashi.jupyterlab
  - sashimi.docusaurus
source:
  homepage: https://ollama.com
  documentation: https://github.com/ollama/ollama/blob/main/README.md
  repository: https://github.com/ollama/ollama
  changelog: https://github.com/ollama/ollama/releases
  license: MIT
  dockerfile: https://github.com/ollama/ollama/blob/main/docker/Dockerfile
  maintainer:
    name: Sushi Kitchen Docs Team
    contact: '@sushi-chef'
    last_reviewed: '2025-02-15'
seo:
  description: Ollama delivers llm api & embeddings in the Hosomaki style and anchors
    bundles like combo.chat-local.
  llm_keywords:
  - Ollama
  - Ollama docker
  - hosomaki.ollama compose
  mcp_tags:
  - cap:cap.llm-api
  - cap:cap.embeddings
mcp:
  preferred_tool: generate_compose
  invocation_examples:
  - description: Generate a Compose file for this service
    command: mcp://sushi-kitchen/generate_compose?select=hosomaki.ollama&environment=docs/manifest/templates/environment-configs/development.yml&network=docs/manifest/templates/network-profiles/open-research.yml
  environment_templates:
  - docs/manifest/templates/environment-configs/development.yml
  network_profiles:
  - docs/manifest/templates/network-profiles/open-research.yml
timeline:
  founded: '2023'
  founders: Dillon Erb, Joey Lieber, and the Ollama Inc. engineering team
  notable_releases:
  - version: '0.1'
    date: 2023-07
    highlight: Initial macOS release with curated model catalog and simple CLI
  - version: '0.2'
    date: 2023-11
    highlight: Introduced server mode and remote API compatibility
  - version: '0.4'
    date: 2024-09
    highlight: Added Windows/Linux support, model conversion pipeline, and GPU scheduling
      improvements
  adoption_highlights:
  - '>100k GitHub stars and a vibrant community catalog of optimized GGUF models'
  - Widely adopted by indie AI builders for air-gapped experimentation
  - Bundled into local agent starter kits across the open-source ecosystem
compliance:
  security_notes:
  - Review environment variable defaults before deployment.
  privacy_notes:
  - Review data retention policies and anonymize user data when exporting logs.
  backup_strategy:
  - Schedule regular snapshots for persistent volumes listed above.
integration_notes:
  configuration_snippets:
  - title: Compose environment overrides
    description: Bootstrap environment variables within docker-compose overrides.
    example: "services:\n                    hosomaki.ollama:\n                  \
      \    environment:\n                        OLLAMA_HOST: 0.0.0.0\nOLLAMA_MODELS:\
      \ /root/.ollama/models\nOLLAMA_KEEP_ALIVE: 24h"
  automation_patterns:
  - Use generate_compose.py to include hosomaki.ollama alongside combo.chat-local.
---

# 🍣 Ollama

> Ollama packages cap.llm-api, cap.embeddings for operators who rely on the Hosomaki lineup. It currently ships inside combos combo.chat-local; bentos bento.ai-agent-foundation; platters platter.hosomaki-core, platter.omakase, platter.voice-first, giving readers a direct path to Compose-ready bundles. Expect CPU ≥ 2 cores · RAM ≥ 4096 MB · Storage ≥ 50 GB · GPU VRAM ≥ 8192 MB, based on the manifest's resource envelope. The enriched front matter above aligns with Sushi Kitchen's manifest exports so MCP servers can cite this roll as an authoritative source.

## 🍱 Quick service snapshot

| Attribute | Details |
| --- | --- |
| **Roll style** | Hosomaki |
| **Service ID** | hosomaki.ollama |
| **Primary capabilities** | cap.llm-api, cap.embeddings |
| **Bundled in** | Combos: combo.chat-local; Bento boxes: bento.ai-agent-foundation; Platters: platter.hosomaki-core, platter.omakase, platter.voice-first |
| **Resource profile** | CPU ≥ 2 cores · RAM ≥ 4096 MB · Storage ≥ 50 GB · GPU VRAM ≥ 8192 MB |
| **Best for** | Local LLM engine with a huge community. |

This manifest-backed snapshot highlights runtime expectations and bundle placement so contributors
can jump straight into Compose planning.

## 🧭 Origin story & evolution

Ollama emerged as a community-driven answer to teams demanding self-hosted alternatives for mission-
critical workflows. Early adopters flocked to it because the Hosomaki style prioritizes pragmatic
defaults and fast iteration, making the service approachable even before Sushi Kitchen captured it
in manifests.

Throughout successive releases the project invested heavily in stability, container ergonomics, and
API compatibility. Those milestones are reflected in today's manifest contract—ports, environment
variables, and health checks are codified so Compose automation works exactly the same on every
deployment.

As Sushi Kitchen matured, Ollama graduated into bundles like platter.hosomaki-core, platter.omakase,
platter.voice-first, proving it could anchor sophisticated scenarios without abandoning its tinkerer
roots. That heritage continues to shape roadmap priorities focused on openness and operator
empowerment.

## 🛠️ Core capabilities & architecture

- Provides capabilities: cap.llm-api, cap.embeddings, enabling downstream bundles to satisfy dependency checks automatically.
- Exposes container ports 11434/tcp, all recorded in contracts.yml so reverse proxies and gateways can wire routing rules without guesswork.
- Persists state via mounts /root/.ollama, which appear both in the Compose template and in the resource guidance above.
- Environment variables are explicitly modeled, letting operators pin secrets and feature flags in infrastructure-as-code pipelines.

## 🍣 Role inside Sushi Kitchen

In combos combo.chat-local the service acts as a plug-and-play building block that aligns tightly with manifest capability requirements. 
Bento boxes bento.ai-agent-foundation lean on this roll to stitch together multi-service solutions without bespoke glue code. 
At platter scale (platter.hosomaki-core, platter.omakase, platter.voice-first) it becomes part of a governed architecture that benefits from shared observability, security, and storage primitives. 
Because contracts declare the capabilities it provides, dependency resolution stays deterministic whether users select rolls manually or let MCP tooling expand bundles for them.

## 🤝 Works great with

- `nigiri.open-webui` — Popular Ollama/LLM chat UI.
- `hosomaki.litellm` — Universal LLM gateway for local + cloud.
- `hosomaki.caddy` — Modern web server with automatic HTTPS & reverse proxy.
- `chirashi.jupyterlab` — Interactive notebooks for DS/AI.
- `sashimi.docusaurus` — Documentation site generator.

## ⚙️ Deployment checklist

1. Use `python generate_compose.py` (or the MCP server) with this roll selected to emit a Compose specification.
2. Populate required environment variables (OLLAMA_HOST, OLLAMA_MODELS, OLLAMA_KEEP_ALIVE, CUDA_VISIBLE_DEVICES) in an `.env` file or Compose overrides.
3. Provision persistent volumes (ollama_data) before first boot to avoid data loss.
4. Validate health by curling `/api/tags` on the running container; adjust intervals if the upstream image recommends.
5. Capture the generated Compose YAML in version control so future updates stay reviewable.

## 📈 Observability & operations

- Track liveness via /api/tags and mirror the interval defined in manifests (30s).
- Forward application logs to `inari.loki` using the shared logging sidecars described in the observability platters.
- Pair with `inari.grafana` or `inari.prometheus` bundles to graph usage patterns and trigger alerts.
- Monitor GPU memory consumption to understand when to scale replicas or upgrade hardware.

## 🔐 Security, privacy, & governance

- Store secrets referenced by environment variables inside `gunkanmaki.vaultwarden` or another secrets roll before deployment.
- Review upstream authentication toggles and disable default credentials as part of initial setup.
- Align log retention with organizational policies; redact user data before exporting traces.

## 🚀 Future roadmap

Watch the upstream Ollama project for roadmap announcements around scalability, plugin ecosystems,
and observability. The Sushi Kitchen manifests track those updates so regenerated documentation
stays aligned with real-world releases.

## 📚 Further reading & learning paths

- [Official documentation](https://github.com/ollama/ollama/blob/main/README.md) — Primary onboarding and admin guides.
- [Source repository](https://github.com/ollama/ollama) — Track releases, issues, and community contributions.
- [Sushi Kitchen manifest](../core/contracts.yml) — Inspect the contract backing this narrative.
- Review related combos and platters in this repository to understand real deployment patterns.
