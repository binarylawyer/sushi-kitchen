# 🍣 Sushi Kitchen — Self-Hosted AI Stack + Website

Sushi Kitchen is a professional-grade, self-hosted AI stack (Docker Compose) plus a Next.js website & community marketplace. Built for:
- home-labbers / advanced self-hosters
- solo developers
- small dev shops
- enterprise departments (team-scoped, privacy-first)

## Highlights
- **Local-first, data-sovereign**: no telemetry, no surprise egress.
- **One-command install** with sane defaults (Lite “core” profile) or Full stack.
- **Composable menu** with **Rolls** (service/agent profiles) & **Platters** (presets/combos).
- **Observability by default** (Grafana, Prometheus, Langfuse) with **Low-Maintenance** profile.
- **Agents + Workflows**: n8n recipes; RAG on `/docs` via pgvector.
- **Next.js + Supabase + Vercel** site: docs, marketplace, community.

## Quick Start (local, core profile)
```bash
git clone https://github.com/<yourorg>/sushi-kitchen.git
cd sushi-kitchen
cp .env.example .env
./install/setup.sh
./install/start.sh

Default endpoints (localhost):

n8n: http://localhost:5678

Grafana: http://localhost:13000 (Full only)

Langfuse: http://localhost:3005 (Full only)

Portainer: http://localhost:9443 (Extras)

ComfyUI: http://localhost:8188 (Media)

## Repo Structure

/apps/web                 # Next.js site (app router, Tailwind UI, Supabase)
/docs                     # Public docs (MD/MDX)
/rolls                    # Agent/service profiles (YAML)
/platters                 # Preset combos (YAML)
/recipes                  # Examples (n8n + prompts)
/workflows                # n8n JSON exports + README
/schemas                  # JSON Schemas (roll/platter)
/prompts                  # System prompt templates
/marketplace              # Seed catalogue metadata + artifacts
/observability            # Grafana dashboards, Prometheus config
.github/workflows         # CI pipelines

## Security & Privacy (tl;dr)

No telemetry. No default egress. Safe defaults.

Secrets via .env (Infisical optional).

Encrypted backups supported (BYOK passphrase).

Non-root containers, minimal caps, private internal network.

## License

Apache-2.0 (see LICENSE).

