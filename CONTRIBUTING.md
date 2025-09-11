# Contributing to Sushi Kitchen

Thank you for helping build a secure, modular, self-hosted AI platform.

## Ground Rules
- Be privacy-first. No surprise egress or analytics.
- Prefer modularity: every new service is optional and off by default.
- Keep agents deterministic where possible; dynamic flows allowed with guardrails.
- Document decisions. Link PRs to the relevant PRD section.

## Development Quickstart
```bash
# Core stack
docker compose --profile core up -d

# Web (local dev)
cd apps/web
pnpm i
pnpm dev
