---
alwaysApply: true
---

# Docs sync from SSOT (tech_stack.mdc)

Goal: keep `docs/` pages aligned with SSOT.

## Rolls
For each `kind: roll`:
- Ensure a page at `docs/rolls/<id>.md`.
- Header contains: `# <name>` and the roll `tagline`.
- Include `description_md` if present.
- List included apps (apps where `roll == <id>`), sorted by `status` (stable → experimental → deprecated) then `name`.
- Show each app’s `badges` inline.

## Apps
For each `kind: app`:
- Ensure a page at `docs/apps/<id>.md`.
- Frontmatter:
id: <id>
title: <name>
status: <status>
badges: [<badges>]
route: <routes[0].ingress or "internal">
- Body (create if missing; preserve any “Notes” section unchanged):
- **Overview** (from `tagline` + `description_md`)
- **Access & Routes** (from `routes` + `security`)
- **Dependencies** (from `depends_on`)
- **Setup** / **Usage** / **Limits** using `docs.anchors` order if present

## Modes
For each `kind: mode`:
- Ensure a page at `docs/modes/<id>.md` summarizing included `rolls` and `apps`.

> Never edit files outside `docs/` and `build/` in this pass.
