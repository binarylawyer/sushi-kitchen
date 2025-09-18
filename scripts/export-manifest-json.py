#!/usr/bin/env python3
"""Sushi Kitchen — Manifest JSON exporter

Converts YAML manifests under ``docs/manifest`` into JSON files for the
website/front-end layer.  Outputs mirror the source folder structure so that
static site generators or SPAs can fetch machine-ready snapshots without
parsing YAML at runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import yaml

MANIFEST_METADATA_FILE = "_metadata.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert manifest YAML to JSON")
    parser.add_argument(
        "--manifest-root",
        type=Path,
        default=Path("docs/manifest"),
        help="Root directory that contains the manifest source files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/manifest/web/api"),
        help="Destination directory for the generated JSON files.",
    )
    parser.add_argument(
        "--include-archives",
        action="store_true",
        help="Also convert files inside the archives/ directory.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output with indentation (default is compact).",
    )
    return parser.parse_args()


def discover_yaml_files(
    manifest_root: Path, include_archives: bool = False
) -> Iterable[Path]:
    """Yield all YAML files under the manifest tree."""
    for extension in ("*.yml", "*.yaml"):
        for path in manifest_root.rglob(extension):
            if not include_archives and "archives" in path.relative_to(manifest_root).parts:
                continue
            yield path


def read_manifest_metadata(manifest_root: Path) -> Dict:
    metadata_path = manifest_root / MANIFEST_METADATA_FILE
    if not metadata_path.exists():
        return {}
    with metadata_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def convert_yaml_file(
    source_path: Path, manifest_root: Path, output_root: Path, pretty: bool
) -> Optional[Tuple[Path, Dict]]:
    """Convert a single YAML file to JSON and return output path + index record."""
    relative_path = source_path.relative_to(manifest_root)
    target_path = (output_root / relative_path).with_suffix(".json")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with source_path.open("r", encoding="utf-8") as src:
            content = yaml.safe_load(src) or {}
    except yaml.YAMLError as err:
        print(f"Skipping {relative_path} (YAML parse error: {err})")
        return None

    with target_path.open("w", encoding="utf-8") as dest:
        if pretty:
            json.dump(content, dest, indent=2, ensure_ascii=False)
            dest.write("\n")
        else:
            json.dump(content, dest, separators=(",", ":"), ensure_ascii=False)

    with source_path.open("rb") as src_bytes:
        sha256 = hashlib.sha256(src_bytes.read()).hexdigest()

    record = {
        "source": str(relative_path).replace("\\", "/"),
        "output": str(target_path.relative_to(output_root.parent)).replace("\\", "/"),
        "sha256": sha256,
    }
    return target_path, record


def write_index(
    index_path: Path,
    records: List[Dict],
    manifest_metadata: Dict,
    manifest_root: Path,
) -> None:
    index_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest_metadata": manifest_metadata.get("manifest_system", {}),
        "source_root": os.path.relpath(manifest_root, start=index_path.parent),
        "files": records,
    }
    with index_path.open("w", encoding="utf-8") as fh:
        json.dump(index_payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main() -> None:
    args = parse_args()
    manifest_root = args.manifest_root.resolve()
    output_root = args.output_dir.resolve()

    if not manifest_root.exists():
        raise SystemExit(f"Manifest root not found: {manifest_root}")

    output_root.mkdir(parents=True, exist_ok=True)

    records: List[Dict] = []
    skipped = 0
    for yaml_file in sorted(discover_yaml_files(manifest_root, args.include_archives)):
        result = convert_yaml_file(yaml_file, manifest_root, output_root, args.pretty)
        if result is None:
            skipped += 1
            continue
        _, record = result
        records.append(record)

    manifest_metadata = read_manifest_metadata(manifest_root)
    index_path = output_root.parent / "manifest-index.json"
    write_index(index_path, records, manifest_metadata, manifest_root)

    print(f"Converted {len(records)} YAML files into JSON under {output_root}")
    if skipped:
        print(f"Skipped {skipped} file(s) due to YAML parse errors or unsupported syntax")
    print(f"Index written to {index_path}")


if __name__ == "__main__":
    main()
