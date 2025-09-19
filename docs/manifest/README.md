# Manifest Files

- **menu-manifest.md** — Human-friendly catalog (Styles → Rolls). No dependency logic.
- **contracts.yml** — Machine contracts per roll (`provides`, `requires`, `suggests`, `conflicts`).
- **combos.yml** — Curated bundles of rolls that “just work.”
- **platters.yml** — Full environments that compose combos (and sometimes extra rolls).
- **badges.yml** — UI labels/tooltips; SVGs live in `assets/badges/`.
- **web/** — Machine-consumable JSON exports for websites and other clients.

Consumers (site/homepage/CLI) can parse these files or rely on the export helper `scripts/export-manifest-json.py`, which mirrors every YAML manifest into JSON under `docs/manifest/web/api/` and publishes an index file for cache-friendly retrieval.
