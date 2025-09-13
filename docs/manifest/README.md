# Manifest Files

- **menu-manifest.md** — Human-friendly catalog (Styles → Rolls). No dependency logic.
- **contracts.yml** — Machine contracts per roll (`provides`, `requires`, `suggests`, `conflicts`).
- **combos.yml** — Curated bundles of rolls that “just work.”
- **platters.yml** — Full environments that compose combos (and sometimes extra rolls).
- **badges.yml** — UI labels/tooltips; SVGs live in `assets/badges/`.

Consumers (site/homepage/CLI) can parse these files or rely on a CI step that emits a merged `menu.json`.
