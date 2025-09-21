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
=======
id: "hosomaki.ollama"
slug: "ollama-local-llm"
style: "Hosomaki"
title: "Ollama Local LLM Server"
status: "recommended"
summary: >-
  Ollama provides a desktop-friendly way to download, run, and serve large language models on your own
  hardware using an OpenAI-compatible API. It powers Sushi Kitchen's most approachable local inference
  experience, delivering private experimentation without giving up modern tooling conveniences.
category:
  menu_section: "Hosomaki"
  service_kind: "inference"
  primary_use_cases:
    - "Private LLM prototyping and evaluation"
    - "Agent backends for chat and workflow orchestration"
capabilities:
  provides:
    - "cap.llm-api"
    - "cap.embeddings"
  requires:
    capabilities: []
    services: []
  suggests:
    - "cap.reverse-proxy"
    - "cap.workflow"
    - "cap.llm-observability"
resources:
  cpu:
    minimum_cores: "2"
    recommended_cores: "4"
  memory:
    minimum_mb: "4096"
    recommended_mb: "8192"
  storage:
    persistent_volumes:
      - name: "ollama_data"
        size_gb: "50"
        purpose: "Model cache and configuration"
  gpu:
    required: "false"
    minimum_vram_mb: "8192"
    notes: "GPU acceleration is strongly recommended for 13B+ models; CPU-only mode works for small 3B variants."
docker:
  image: "ollama/ollama:latest"
  tag_strategy: "Track upstream latest tag; pin to digests for production stability"
  ports:
    - container: 11434
      host_range: "11434"
      protocol: "tcp"
      description: "OpenAI-compatible inference API"
  volumes:
    - name: "ollama_data"
      mount: "/root/.ollama"
      type: "named"
  environment:
    required:
      OLLAMA_HOST: "0.0.0.0"
      OLLAMA_MODELS: "/root/.ollama/models"
      OLLAMA_KEEP_ALIVE: "24h"
    optional:
      CUDA_VISIBLE_DEVICES: "${CUDA_VISIBLE_DEVICES:-all}"
      OLLAMA_ORIGINS: "https://your-domain.example.com"
observability:
  healthcheck:
    endpoint: "/api/tags"
    interval: "30s"
    retries: 3
  metrics:
    enabled: "false"
    collection_notes: "Expose request metrics via reverse proxy (e.g., Caddy) or wrap with LiteLLM telemetry."
  logging:
    retention_days: "14"
    recommended_sinks:
      - "nigiri.loki-promtail"
dependencies:
  data_flow:
    inbound:
      - description: "Receives HTTP/gRPC requests from chat UIs, automation tools, and gateways"
        source: "hosomaki.litellm, nigiri.open-webui, hosomaki.n8n"
    outbound:
      - description: "Streams token responses and embeddings back to callers over HTTP"
        target: "Client services that implement OpenAI-compatible APIs"
  configuration_prerequisites:
    - "Download at least one model via `ollama pull` after the container starts"
    - "Set CUDA visibility to match available GPUs when deploying on multi-tenant hosts"
    - "Optionally front with `hosomaki.caddy` for TLS and access controls"
  failure_modes:
    - "Model downloads can exhaust disk space; monitor the `ollama_data` volume capacity"
    - "GPU memory exhaustion aborts inference; choose smaller models or limit concurrency"
    - "Long-running prompts may time out behind proxies—tune keep-alive settings accordingly"
bundles:
  combos:
    - "combo.chat-local"
  bento_boxes:
    - "bento.ai-agent-foundation"
  platters: []
  pairs_well_with:
    - "nigiri.open-webui"
    - "hosomaki.litellm"
    - "hosomaki.anythingllm"
    - "futomaki.qdrant"
    - "gunkanmaki.vaultwarden"
source:
  homepage: "https://ollama.com"
  documentation: "https://github.com/ollama/ollama/blob/main/README.md"
  repository: "https://github.com/ollama/ollama"
  changelog: "https://github.com/ollama/ollama/releases"
  license: "MIT"
  dockerfile: "https://github.com/ollama/ollama/blob/main/docker/Dockerfile"
  maintainer:
    name: "Sushi Kitchen Docs Team"
    contact: "@sushi-chef"
    last_reviewed: "2025-02-15"
seo:
  description: >-
    Run large language models locally with Ollama's OpenAI-compatible server for private, GPU-accelerated inference.
  llm_keywords:
    - "local llm server"
    - "openai compatible offline inference"
  mcp_tags:
    - "workflow:inference"
    - "capability:cap.llm-api"
mcp:
  preferred_tool: "generate_compose"
  invocation_examples:
    - description: "Stand up a local chat stack with Ollama and Open WebUI"
      command: >-
        mcp://sushi-kitchen/generate_compose?select=combo.chat-local&environment=docs/manifest/templates/environment-configs/development.yml&network=docs/manifest/templates/network-profiles/open-research.yml
    - description: "Provision Ollama alone for embedding generation"
      command: >-
        mcp://sushi-kitchen/generate_compose?select=hosomaki.ollama&environment=docs/manifest/templates/environment-configs/development.yml&network=docs/manifest/templates/network-profiles/open-research.yml
  environment_templates:
    - "docs/manifest/templates/environment-configs/development.yml"
    - "docs/manifest/templates/environment-configs/gpu-workstation.yml"
  network_profiles:
    - "docs/manifest/templates/network-profiles/open-research.yml"
    - "docs/manifest/templates/network-profiles/business-confidential.yml"
timeline:
  founded: "2023"
  founders: "Dillon Erb, Joey Lieber, and the Ollama Inc. engineering team"
  notable_releases:
    - version: "0.1"
      date: "2023-07"
      highlight: "Initial macOS release with curated model catalog and simple CLI"
    - version: "0.2"
      date: "2023-11"
      highlight: "Introduced server mode and remote API compatibility"
    - version: "0.4"
      date: "2024-09"
      highlight: "Added Windows/Linux support, model conversion pipeline, and GPU scheduling improvements"
  adoption_highlights:
    - ">100k GitHub stars and a vibrant community catalog of optimized GGUF models"
    - "Widely adopted by indie AI builders for air-gapped experimentation"
    - "Bundled into local agent starter kits across the open-source ecosystem"
compliance:
  security_notes:
    - "Review release notes for security fixes; upstream ships frequent patch releases"
    - "Restrict API exposure with `hosomaki.caddy` or firewall rules to avoid unauthorized model access"
  privacy_notes:
    - "Models and prompts stay on-disk; ensure encrypted volumes when handling sensitive data"
  backup_strategy:
    - "Snapshot the `ollama_data` volume after major model downloads to speed up restores"
integration_notes:
  configuration_snippets:
    - title: "Expose Ollama through LiteLLM"
      description: "Route multi-model traffic via LiteLLM while keeping Ollama local"
      example: |-
        services:
          litellm:
            environment:
              LITELLM_ROUTES: |
                {
                  "ollama-chat": {
                    "host": "http://ollama:11434",
                    "model_list": ["llama3", "mistral"],
                    "api_key": "${LITELLM_PROXY_KEY}"
                  }
                }
  automation_patterns:
    - "Schedule nightly `ollama pull` updates via `hosomaki.n8n` to keep local models fresh"
    - "Use `futomaki.qdrant` to store embeddings produced by Ollama for downstream semantic search"
---

# 🍣 Ollama Local LLM Server

Ollama packages the hard parts of running local large language models—model downloads, quantized
runtimes, and an OpenAI-compatible API—into a single binary and container image. Operators get a
sensible default catalog and quick CLI, while Sushi Kitchen leverages the Dockerized version to ship
private inference endpoints in minutes. For teams that want the convenience of hosted AI with the
privacy of on-prem hardware, Ollama delivers a gentle on-ramp.

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
=======
| **Bundled in** | combo.chat-local · bento.ai-agent-foundation |
| **Resource profile** | 2+ CPU cores · 4–8 GB RAM · Optional 8 GB+ VRAM |
| **Best for** | Builders testing models privately, agent developers, privacy-conscious researchers |

Ollama ships a generous default cache location and keeps models on persistent storage so you are not
forced to redownload multi-gigabyte assets after container restarts. Because the API mirrors OpenAI's
endpoints, most SDKs and low-code tools work without modification—ideal for rapid prototyping.

## 🧭 Origin story & evolution

Ollama emerged in mid-2023, when founders Dillon Erb and Joey Lieber set out to make local AI models
as approachable as cloud-hosted APIs. Early releases targeted macOS laptops and emphasized a curated
model catalog, simple CLI commands, and a tightly-integrated download experience. The community quickly
embraced the idea of running quantized GGUF models without wrestling with Python environments.

Within a few months, the project expanded beyond the desktop. By late 2023, Ollama added a headless
server mode, enabling remote API access, containers, and multi-user setups. This release also introduced
OpenAI-compatible routes, making the tool a drop-in replacement for popular SDKs and SaaS workflows.
As the model zoo exploded, Ollama's maintainers focused on conversion pipelines and GPU scheduling to
handle everything from tiny instruct models to 70B parameter giants.

The pace has not slowed. Through 2024 the project gained Windows and Linux installers, ARM builds, and
a thriving ecosystem of community-tuned models. Its GitHub repository surpassed the hundred-thousand
star mark as enterprises and hobbyists alike adopted it for air-gapped experimentation. Today, Ollama is
positioned as the friendliest bridge between hobby-friendly laptops and enterprise-grade inference rigs.

## 🛠️ Core capabilities & architecture

- **OpenAI-compatible endpoints** provide `/v1/chat/completions`, `/v1/completions`, and `/v1/embeddings`
  APIs, allowing existing clients to switch without code changes.
- **Model management CLI** handles downloads (`ollama pull`), updates, and deletions, storing quantized
  GGUF artifacts in the persistent `ollama_data` volume.
- **Runtime flexibility** supports CPU-only execution for smaller models and GPU acceleration via CUDA,
  automatically selecting optimized runners when GPUs are available.
- **Prompt streaming and templates** enable token-by-token responses and custom system prompts, useful for
  orchestrators such as `hosomaki.n8n`.
- **Extensibility hooks** expose configuration for custom repositories, offline mirrors, and secure model
  serving behind reverse proxies or API gateways.

## 🍣 Role inside Sushi Kitchen

Inside Sushi Kitchen, Ollama anchors the Hosomaki lineup as the fastest path to local inference. The
`combo.chat-local` pairing with `nigiri.open-webui` turns it into a ChatGPT-style experience, while the
`bento.ai-agent-foundation` set couples Ollama with `hosomaki.n8n`, Supabase, and Caddy to deliver a
full agent backend. Because it exports both chat completions and embeddings, Ollama can satisfy the
capabilities that `hosomaki.anythingllm` and `futomaki.qdrant` request without leaving your network.

When you need deterministic performance or advanced GPU scheduling, you might graduate to `hosomaki.vllm`
or `hosomaki.triton`. But for experiments, demos, and lightweight production tasks, Ollama strikes the
right balance of simplicity and power.

## 🤝 Works great with

- `nigiri.open-webui` – Delivers a polished chat UI that speaks directly to Ollama's API.
- `hosomaki.litellm` – Provides model routing, rate limiting, and observability while delegating requests
  to Ollama.
- `hosomaki.anythingllm` – Uses Ollama for both conversation and embeddings in document-grounded chat.
- `futomaki.qdrant` – Stores embeddings generated by Ollama for semantic search workflows.
- `gunkanmaki.vaultwarden` – Protects API keys and service secrets when exposing Ollama beyond localhost.

## ⚙️ Deployment checklist

1. Generate a Compose file selecting either `hosomaki.ollama` directly or a bundle like
   `combo.chat-local` via `generate_compose.py` or the Sushi Kitchen MCP server.
2. Provision persistent storage for the `ollama_data` volume with at least 50 GB of space; expand if you
   plan to host multiple 13B+ models.
3. Set GPU visibility (`CUDA_VISIBLE_DEVICES`) to match the hardware profile, or explicitly disable it on
   CPU-only hosts to avoid startup warnings.
4. Launch the stack and run `docker exec -it ollama ollama pull llama3` (or your preferred model) to
   seed the cache.
5. Validate health with `curl http://localhost:11434/api/tags` and send a sample chat completion to ensure
   streaming works through your chosen proxy or gateway.

## 📈 Observability & operations

Ollama includes a lightweight health endpoint but no native metrics collector. Pair it with
`nigiri.loki-promtail` to aggregate logs and forward them into the Sushi Kitchen monitoring pipeline.
If you require per-model analytics, run traffic through `hosomaki.litellm` or instrument your reverse
proxy to record response times and token usage. Scale vertically by adding GPU memory; horizontally, run
multiple replicas with a shared model volume when using the same host-level GPU via MIG or virtualization.

## 🔐 Security, privacy, & governance

By default, Ollama listens on all interfaces. Place it behind `hosomaki.caddy` or another reverse proxy
for TLS termination and access control, and store API secrets in `gunkanmaki.vaultwarden`. Because models
and prompts stay on disk, encrypt the `ollama_data` volume and restrict host access. Regularly update the
image to pick up mitigations for third-party library CVEs and review model licenses to ensure your usage
complies with upstream restrictions.

## 🚀 Future roadmap

The Ollama team continues to invest in cross-platform support, improved GPU scheduling, and enterprise
features like RBAC and model repository mirroring. Ongoing efforts to support multimodal inputs and
structured tool-calling will make it even more attractive for agent frameworks. Keep an eye on the
release notes for expanded quantization support and memory optimizations that reduce hardware
requirements.

## 📚 Further reading & learning paths

- [Ollama Documentation – Getting Started](https://github.com/ollama/ollama/blob/main/README.md)
- [Ollama Release Notes](https://github.com/ollama/ollama/releases)
- [Local-first LLM Pipelines with Ollama and Qdrant (Blog, 2024)](https://qdrant.tech/articles/)
- [Running Ollama with Open WebUI (Community Tutorial, 2024)](https://github.com/open-webui/open-webui/wiki)
- Sushi Kitchen recipe: `docs/manifest/examples/agents/local-agent-playbook.md` (add once published)

Ready for more? Explore `hosomaki.litellm` next to learn how to multiplex Ollama with cloud models and
layer in request analytics.
