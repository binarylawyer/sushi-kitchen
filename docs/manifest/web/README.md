# Web Data Exports

This directory hosts machine-consumable exports of the manifest system for the Sushi Kitchen website and any other UI surfaces.  The source manifests under `docs/manifest/` remain the single source of truth.  A helper script converts the YAML bundles and templates into JSON that can be fetched directly by front-end code.

## Folder layout

```
web/
├── README.md               # This guide
├── api/                    # JSON mirrors of the manifest YAML
│   └── ...
└── manifest-index.json     # Catalog of generated files with hashes and metadata
```

* `api/` mirrors the structure of the manifest tree.  For example, `core/combos.yml` becomes `web/api/core/combos.json`.
* `manifest-index.json` lists every exported file, the manifest revision it was derived from, and a SHA-256 digest for cache validation.

## Generating the exports

Use the `scripts/export-manifest-json.py` helper to regenerate the JSON snapshot whenever any YAML manifest changes:

```bash
python scripts/export-manifest-json.py \
  --manifest-root docs/manifest \
  --output-dir docs/manifest/web/api
```

The script writes the converted JSON files and refreshes `manifest-index.json`.  By default it skips the archived manifests; add `--include-archives` if you need historical data.

## Using the data in a website

1. **Fetch the index** – Load `docs/manifest/web/manifest-index.json` to discover the available resources and the manifest metadata.
2. **Pull only what you need** – Each entry provides a relative path to the JSON export.  Front ends can request the individual files they require (for example, `web/api/core/bento_box.json`).
3. **Validate freshness** – Compare the stored SHA-256 digest against the file contents or watch the `generated_at` timestamp to trigger client-side cache invalidation.
4. **Automate regeneration** – Wire the export script into CI so that new JSON snapshots land alongside every manifest change, keeping the website in sync with the source repository.

## Extending the pipeline

The exporter is schema-agnostic: any `.yml` or `.yaml` file under the manifest root is mirrored into JSON.  If additional normalization is required (for example, flattening Markdown tables or computing dependency graphs), add a post-processing step or extend the script with custom handlers per directory.

