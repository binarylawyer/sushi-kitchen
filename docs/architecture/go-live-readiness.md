# Sushi Kitchen Go-Live Readiness Assessment

## Current Architecture Snapshot
- The platform is still organized around the three-repository model (SSOT core, FastAPI service, and web frontend). Recent documentation confirms this split but the implementation has diverged, especially in the manifest and automation layers.
- The manifest system now lives under `docs/manifest/core/` and feeds JSON exports in `docs/manifest/web/api/`, giving us a static snapshot to serve to clients.

## Sushi Kitchen API (FastAPI) Status

### Integration gaps
- `app/main.py` does not import `json` even though `/api/v1/bundle` reads JSON files, and all collection endpoints expect dict-shaped component data that no longer matches the exported bundle structure.
- `ManifestOrchestrator` still shells out to `generate-compose.py` with `--manifest-dir docs/manifest`, but the manifest YAMLs have moved into `docs/manifest/core`. Even if the path were corrected, the script expects the old schema (platters with `includes`, direct roll lookups) and will error against the new documents.
- The orchestrator’s fallback loader assumes the exported JSON writes `platters`, `combos`, and `rolls` as dictionaries. The exporter now produces list-based collections and puts rolls under `services`, so the coercion logic returns empty data.

### Data model issues
- Several Pydantic models in `app/models.py` use mutable defaults (`List[str] = []`). If any request mutates these in place, the change would leak across requests.
- Validation logic in `ManifestOrchestrator.validate_configuration` checks for `service_config.get('networks', [])`, but the compose generator never normalizes services into the new schema, so validation cannot yet be exercised end-to-end.

### Automation pipeline
- `scripts/generate-compose.py` and `scripts/generate-api-bundle.py` both still target the legacy manifest layout (`docs/manifest/*.yml`) and fields such as `provides` and `includes`. They need a schema adapter layer (or a manifest export step) before the API can reliably invoke them.
- The CI workflow that was meant to place `generated/api-bundle.json` inside `sushi-kitchen-api/` relies on `generate-api-bundle.py`. Until that script understands the new manifest format, the API cannot serve prebuilt bundles or TypeScript types.

## SSOT Repository Status
- `docs/manifest/core/platters.yml` now describes platters in terms of `combos` and `additional_services`. The compose generator does not know how to translate these into individual service IDs.
- `docs/manifest/core/combos.yml` introduces richer metadata (e.g., `resource_estimate`, `success_criteria`). None of that is surfaced through the API bundle or compose scripts yet.
- The JSON export pipeline (`scripts/export-manifest-json.py`) successfully mirrors the manifest tree into `docs/manifest/web/api/`. This JSON is the most reliable source for clients today, but no runtime code is consuming it.

## Web Frontend Status
- The `sushi-kitchen-web` repository contains only a README stub. There is no scaffolded app, no generated types, and no API client. We cannot demo or validate end-to-end flows without implementing the frontend.

## Path to Launch
1. **Schema Alignment**
   - Add a lightweight schema adapter so `generate-compose.py` and the API bundler can ingest the new manifests (likely by pointing them at the exported JSON instead of raw YAML).
   - Update `ManifestOrchestrator` to read from the generated bundle (or exported JSON) and translate list-based collections into keyed lookups for the API responses.
2. **API Hardening**
   - Fix missing imports, replace mutable defaults, and improve error reporting when external scripts fail.
   - Extend validation to cover the richer metadata (resource requirements, success criteria) and ensure network/security overlays match the new profiles.
3. **CI/CD Wiring**
   - Refresh the manifest-sync workflow so that every SSOT change produces an updated API bundle and TypeScript types, then publish them into the API repo.
4. **Frontend Implementation**
   - Scaffold the web app, pull the generated types, and implement catalog browsing plus compose generation flows against the updated API.
5. **Cross-Repo Contract Tests**
   - Create smoke tests that clone all three repositories, run the exporter + bundler, start the API, and hit key endpoints with sample data.

Once those items are complete—and we verify compose generation against a few representative platters—the platform will be ready for a public launch.
