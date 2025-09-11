# Developer Guide

## Web
```bash
cd apps/web
pnpm i
pnpm dev

- Next.js (app router), Tailwind, Supabase client
- Env: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY

## Validating Configs

pnpm -w lint
pnpm -w validate:schema
docker compose config

## Adding Dashboards

- Drop JSON into /observability/grafana/dashboards
- Update provisioning as needed