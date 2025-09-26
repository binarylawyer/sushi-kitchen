---
schema_version: 1.0.0
content_version: 0.1.0
last_updated: "TODO: YYYY-MM-DD"
manifest_ref:
  contracts: "docs/manifest/core/contracts.yml#services.TODO-service-id"
  menu: "docs/manifest/core/menu-manifest.md#styles.TODO-style.TODO-service-id"
assets: []
export:
  sections:
    quick_service_snapshot:
      heading: "🍱 Quick service snapshot"
      anchor: "quick-service-snapshot"
    origin_story:
      heading: "🧭 Origin story & evolution"
      anchor: "origin-story-evolution"
    capabilities:
      heading: "🛠️ Core capabilities & architecture"
      anchor: "core-capabilities-architecture"
    role:
      heading: "🍣 Role inside Sushi Kitchen"
      anchor: "role-inside-sushi-kitchen"
    partnerships:
      heading: "🤝 Works great with"
      anchor: "works-great-with"
    deployment:
      heading: "⚙️ Deployment checklist"
      anchor: "deployment-checklist"
    observability:
      heading: "📈 Observability & operations"
      anchor: "observability-operations"
    security:
      heading: "🔐 Security, privacy, & governance"
      anchor: "security-privacy-governance"
    roadmap:
      heading: "🚀 Future roadmap"
      anchor: "future-roadmap"
    further_reading:
      heading: "📚 Further reading & learning paths"
      anchor: "further-reading-learning-paths"
id: "TODO: manifest service id (e.g., hosomaki.ollama)"
slug: "TODO: derived slug (e.g., hosomaki-ollama)"
id: "TODO: manifest service id (e.g., hosomaki.ollama)"
slug: "TODO: url-friendly-slug"
style: "TODO: Hosomaki | Futomaki | Nigiri | Gunkanmaki | Sashimi | Temaki | Chirashi | Inari | Uramaki | Otsumami"
title: "TODO: Display name for this roll"
status: "TODO: recommended | optional | experimental"
summary: >-
  TODO: 2-3 sentence elevator pitch that mirrors the entry in `core/menu-manifest.md`.
category:
  menu_section: "TODO: style name from menu-manifest"
  service_kind: "TODO: runtime classification (e.g., inference, workflow, storage)"
  primary_use_cases:
    - "TODO: highlight a practical use case"
    - "TODO: optional additional use case"
  TODO: 2-3 sentence elevator pitch that mirrors the entry in `core/menu-manifest.md`
category:
  menu_section: "TODO: matching section from menu-manifest"
  service_kind: "TODO: e.g., inference, workflow, storage"
  primary_use_cases:
    - "TODO: short use case"
    - "TODO: additional use case"
capabilities:
  provides:
    - "TODO: cap.* identifiers from contracts"
  requires:
    capabilities:
      - "TODO: cap.* dependency (omit if none)"
    services:
      - "TODO: explicit service dependency (omit if none)"
  suggests:
    - "TODO: optional companion capability"
resources:
  cpu:
    minimum_cores: TODO
    recommended_cores: TODO
  memory:
    minimum_mb: TODO
    recommended_mb: TODO
  storage:
    persistent_volumes:
      - name: "TODO"
        size_gb: TODO
        purpose: "TODO"
  gpu:
    required: TODO
    minimum_vram_mb: "TODO if gpu required"
    notes: "TODO: describe GPU expectations or CPU fallback"
docker:
  image: "TODO: upstream image reference"
  tag_strategy: "TODO: track-upstream | pin-to-digest"
      - "TODO: cap.* dependencies (if any)"
    services:
      - "TODO: service ids this roll explicitly depends on"
  suggests:
    - "TODO: optional caps or companion services"
resources:
  cpu:
    minimum_cores: "TODO: align with contracts.yml"
    recommended_cores: "TODO"
  memory:
    minimum_mb: "TODO"
    recommended_mb: "TODO"
  storage:
    persistent_volumes:
      - name: "TODO"
        size_gb: "TODO"
        purpose: "TODO"
  gpu:
    required: "TODO: true | false"
    minimum_vram_mb: "TODO if gpu required"
    notes: "TODO: guidance on GPU usage or CPU-only fallback"
docker:
  image: "TODO: upstream image reference"
  tag_strategy: "TODO: e.g., pin to digest, track latest"
  ports:
    - container: TODO
      host_range: "TODO"
      protocol: "TODO"
      description: "TODO"
  volumes:
    - name: "TODO volume id"
      mount: "TODO container path"
      type: "TODO named | bind"
  environment:
    required:
      KEY: "TODO value or variable reference"
    optional:
      OPTIONAL_KEY: "TODO optional setting"
observability:
  healthcheck:
    endpoint: "TODO: /health"
    interval: "TODO: 30s"
    retries: TODO
  metrics:
    enabled: "TODO: true | false"
    collection_notes: "TODO"
  logging:
    retention_days: TODO
    recommended_sinks:
      - "TODO: e.g., inari.loki"
dependencies:
  data_flow:
    inbound:
      - description: "TODO: describe upstream requirement"
        source: "TODO: capability or service"
    outbound:
      - description: "TODO: describe downstream output"
        target: "TODO: capability or service"
    retention_days: "TODO"
    recommended_sinks:
      - "TODO: e.g., loki-promtail"
dependencies:
  data_flow:
    inbound:
      - description: "TODO"
        source: "TODO"
    outbound:
      - description: "TODO"
        target: "TODO"
  configuration_prerequisites:
    - "TODO: secrets, API keys, domain setup"
  failure_modes:
    - "TODO: known issues and mitigations"
bundles:
  combos:
    - id: "TODO: combo id"
      name: "TODO: combo name"
  bento_boxes:
    - id: "TODO: bento id"
      name: "TODO: bento name"
  platters:
    - id: "TODO: platter id"
      name: "TODO: platter name"
    - "TODO: combo ids using this roll"
  bento_boxes:
    - "TODO: bento ids using this roll"
  platters:
    - "TODO: platter ids using this roll"
  pairs_well_with:
    - "TODO: manifest service ids for cross-links"
source:
  homepage: "TODO: https://"
  documentation: "TODO: https://"
  repository: "TODO: https://"
  changelog: "TODO: https://"
  changelog: "TODO: https:// or release notes"
  license: "TODO: license name"
  dockerfile: "TODO: upstream Dockerfile path if relevant"
  maintainer:
    name: "TODO: internal owner"
    contact: "TODO: handle or email"
    last_reviewed: "TODO: YYYY-MM-DD"
seo:
  description: >-
    TODO: 160-character meta description for search indices.
    TODO: 160-character meta description for search indices
  llm_keywords:
    - "TODO: phrase targeted at LLM retrieval"
    - "TODO: alternate keyword"
  mcp_tags:
    - "TODO: capability or workflow tags for MCP directories"
mcp:
  preferred_tool: "generate_compose"
  invocation_examples:
    - description: "TODO: what the user wants to build"
      command: >-
        mcp://sushi-kitchen/generate_compose?select=TODO-id&environment=docs/manifest/templates/environment-configs/development.yml&network=docs/manifest/templates/network-profiles/open-research.yml
  environment_templates:
    - "docs/manifest/templates/environment-configs/development.yml"
  network_profiles:
    - "docs/manifest/templates/network-profiles/open-research.yml"
timeline:
  founded: "TODO: YYYY"
  founders: "TODO: name(s)"
  notable_releases:
    - version: "TODO"
      date: "TODO: YYYY-MM"
      highlight: "TODO: release milestone"
  adoption_highlights:
    - "TODO: notable companies or community stats"
compliance:
  security_notes:
    - "TODO: CVEs, update cadence, auth requirements"
  privacy_notes:
    - "TODO: data handling guidance"
  backup_strategy:
    - "TODO: recommended backup approach for volumes"
integration_notes:
  configuration_snippets:
    - title: "TODO: example integration"
      description: "TODO: what the snippet accomplishes"
      example: |-
        TODO: YAML or shell snippet demonstrating integration
  automation_patterns:
    - "TODO: describe automation scenario"
    - "TODO: another automation idea"
---

<!--
Fill in the metadata above before writing narrative content. The YAML front matter is consumed by
static-site generators and MCP tooling; keep keys consistent with contracts.yml and menu-manifest.md.
-->

# 🍣 {{ Roll Display Name }}

> Replace this block with a concise executive summary (3-4 sentences) highlighting what the roll does,
> who benefits, and why it belongs in the Sushi Kitchen ecosystem.

## 🍱 Quick service snapshot

| Attribute | Details |
| --- | --- |
| **Roll style** | {{ style }} |
| **Service ID** | {{ manifest id }} |
| **Primary capabilities** | {{ cap list }} |
| **Bundled in** | {{ combos/bentos/platters }} |
| **Resource profile** | {{ CPU / RAM / GPU summary }} |
| **Best for** | {{ target personas }} |

_Add 2-3 sentences below the table calling out anything special about setup requirements,
licensing, or deployment modes._

## 🧭 Origin story & evolution

Write a rich, historical narrative that is at least three paragraphs long. Cover:
1. **Founding context** – when the project started, by whom, and what problem they set out to solve.
2. **Milestone releases** – highlight breakthrough features or architectural shifts.
3. **Community & adoption** – describe growth, notable users, or ecosystem contributions.

Close the section with a sentence about how the project's past shapes its current direction.

## 🛠️ Core capabilities & architecture

Provide a deep dive into how the service works today:
- Enumerate critical features with explanations (3-5 bullets, full sentences).
- Explain architectural components (e.g., runtime, storage, external dependencies).
- Mention supported deployment modes or configuration profiles relevant to Sushi Kitchen.

## 🍣 Role inside Sushi Kitchen

Describe how this roll integrates with other offerings:
- Map capability requirements to actual companion services (databases, proxies, GPUs, etc.).
- Reference bundles from the front matter and explain what problem each bundle solves.
- Include guidance on when to pick this roll over alternatives in the same menu section.

## 🤝 Works great with

List 3-5 complementary rolls or external services, each with a one-sentence rationale. Use manifest IDs
(e.g., `futomaki.qdrant`) so documentation tooling can auto-link the references.

## ⚙️ Deployment checklist

Provide a numbered list walking operators from `generate_compose.py` (or the MCP server) to a ready
service. Mention environment variables, secrets, migrations, and post-deploy validation steps.

## 📈 Observability & operations

Explain how to keep the service healthy:
- Describe built-in health endpoints, metrics, and logs.
- Recommend Sushi Kitchen monitoring rolls (Grafana, Loki, etc.) with manifest IDs.
- Include common scaling strategies or backup guidance tied to the resources defined in contracts.

## 🔐 Security, privacy, & governance

Detail authentication options, data handling considerations, and any compliance notes. Call out
configuration flags that toggle privacy modes or audit logs. Mention how secrets should be stored
(e.g., `gunkanmaki.vaultwarden`).

## 🚀 Future roadmap

Summarize publicly-announced upstream plans or areas the community is investing in. Tie predictions
to what Sushi Kitchen operators should watch for (e.g., upcoming API changes, plugin ecosystems).

## 📚 Further reading & learning paths

Curate a set of authoritative resources:
- Official documentation sections for onboarding, admin guides, and API references.
- High-quality blog posts, conference talks, or tutorials (label with publication + year).
- Sushi Kitchen-specific recipes or workflows (`docs/manifest/examples/...`) when available.

Conclude with a short call-to-action inviting contributions or suggesting the next roll to explore.
