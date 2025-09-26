"""Roll narrative generator for Sushi Kitchen services.

This module loads the manifest contracts, combos, bento boxes, platters,
and menu metadata to emit richly annotated Markdown documentation for a
single roll.  The resulting document includes comprehensive YAML front
matter aligned with the manifest schema so downstream tooling (MCP
servers, static exporters) can convert the narrative into JSON easily.

Usage (CLI):
    python docs/manifest/narratives/rolls/generate_roll.py hosomaki.ollama

Tests import ``RollTemplateGenerator`` directly to exercise the data
extraction and rendering helpers.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import textwrap
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import yaml


MANIFEST_ROOT = Path("docs/manifest/core")
NARRATIVE_ROOT = Path("docs/manifest/narratives/rolls")
FRONT_MATTER_SCHEMA_VERSION = "1.0.0"
DEFAULT_CONTENT_VERSION = "0.1.0"


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        loader = yaml.safe_load_all(handle)
        try:
            return next(loader)
        except StopIteration:
            return {}


class RollMenuEntry:
    """Lightweight container for menu metadata."""

    def __init__(self, style: str, data: Mapping[str, Any]) -> None:
        self.style = style
        self.data = data

    @property
    def name(self) -> str:
        return str(self.data.get("name", ""))

    @property
    def status(self) -> str:
        return str(self.data.get("status", ""))

    @property
    def notes(self) -> str:
        return str(self.data.get("notes", ""))


class RollTemplateGenerator:
    """Generate Markdown narratives for manifest-defined rolls."""

    def __init__(
        self,
        manifest_root: Path | str = MANIFEST_ROOT,
        narrative_root: Path | str = NARRATIVE_ROOT,
    ) -> None:
        self.manifest_root = Path(manifest_root)
        self.narrative_root = Path(narrative_root)
        self.contracts = _load_yaml(self.manifest_root / "contracts.yml")
        self.services: Mapping[str, Any] = self.contracts.get("services", {})
        self.combos_data = _load_yaml(self.manifest_root / "combos.yml")
        self.bento_data = _load_yaml(self.manifest_root / "bento-box.yml")
        self.platters_data = _load_yaml(self.manifest_root / "platters.yml")
        self.menu_data = _load_yaml(self.manifest_root / "menu-manifest.md")

        self.combos: Dict[str, Mapping[str, Any]] = {
            combo["id"]: combo for combo in self.combos_data.get("combos", [])
        }
        self.bentos: Dict[str, Mapping[str, Any]] = {
            box["id"]: box for box in self.bento_data.get("bento_boxes", [])
        }
        self.platters: Dict[str, Mapping[str, Any]] = {
            platter["id"]: platter for platter in self.platters_data.get("platters", [])
        }

        self.roll_catalog: Dict[str, RollMenuEntry] = {}
        for style in self.menu_data.get("styles", []):
            style_name = style.get("name", "")
            for roll in style.get("rolls", []):
                roll_id = roll.get("id")
                if not roll_id:
                    continue
                self.roll_catalog[roll_id] = RollMenuEntry(style=style_name, data=roll)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build_roll_markdown(self, service_id: str) -> str:
        service = self._get_service_contract(service_id)
        menu_entry = self._get_menu_entry(service_id)
        bundle_membership = self._collect_bundle_membership(service_id)
        front_matter = self._build_front_matter(service_id, service, menu_entry, bundle_membership)
        body = self._render_body(service_id, service, menu_entry, bundle_membership)
        yaml_block = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True).strip()
        return f"---\n{yaml_block}\n---\n\n{body}"

    def write_roll(self, service_id: str, output_dir: Path | str | None = None) -> Path:
        output_dir = Path(output_dir) if output_dir else self.narrative_root
        output_dir.mkdir(parents=True, exist_ok=True)
        markdown = self.build_roll_markdown(service_id)
        target = output_dir / f"{service_id}.md"
        target.write_text(markdown, encoding="utf-8")
        return target

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get_service_contract(self, service_id: str) -> Mapping[str, Any]:
        if service_id not in self.services:
            raise KeyError(f"Service '{service_id}' not found in contracts.yml")
        return self.services[service_id]

    def _get_menu_entry(self, service_id: str) -> RollMenuEntry:
        if service_id not in self.roll_catalog:
            raise KeyError(f"Service '{service_id}' is missing from menu-manifest.md")
        return self.roll_catalog[service_id]

    def _collect_bundle_membership(self, service_id: str) -> Dict[str, List[Dict[str, str]]]:
        combos: List[Dict[str, str]] = []
        for combo in self.combos.values():
            includes = combo.get("includes", []) + combo.get("optional", [])
            if service_id in includes:
                combos.append({"id": combo["id"], "name": combo.get("name", "")})
        bento_boxes: List[Dict[str, str]] = []
        for box in self.bentos.values():
            includes = box.get("includes", []) + box.get("optional", [])
            if service_id in includes:
                bento_boxes.append({"id": box["id"], "name": box.get("name", "")})
        platters: List[Dict[str, str]] = []
        combos_with_service = {combo["id"] for combo in combos}
        for platter in self.platters.values():
            combo_ids = platter.get("combos", [])
            additional_services = platter.get("additional_services", [])
            include = False
            if service_id in additional_services:
                include = True
            elif combos_with_service and any(cid in combos_with_service for cid in combo_ids):
                include = True
            if include:
                platters.append({"id": platter["id"], "name": platter.get("name", "")})
        return {
            "combos": sorted(combos, key=lambda item: item["id"]),
            "bento_boxes": sorted(bento_boxes, key=lambda item: item["id"]),
            "platters": sorted(platters, key=lambda item: item["id"]),
        }

    def _build_front_matter(
        self,
        service_id: str,
        service: Mapping[str, Any],
        menu_entry: RollMenuEntry,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
    ) -> Dict[str, Any]:
        provides = list(service.get("provides", []))
        requires_raw = list(service.get("requires", []))
        suggests = list(service.get("suggests", []))
        req_capabilities = [item for item in requires_raw if isinstance(item, str) and item.startswith("cap.")]
        req_services = [item for item in requires_raw if isinstance(item, str) and not item.startswith("cap.")]

        resources = service.get("resource_requirements", {})
        cpu_min = resources.get("cpu_cores")
        mem_min = resources.get("memory_mb")
        storage_min = resources.get("storage_gb")
        gpu_min = resources.get("gpu_memory_mb")
        gpu_required = bool(service.get("device_requests")) or bool(resources.get("gpu_required"))

        env_vars = service.get("environment", {})
        ports = service.get("ports", [])
        volumes = service.get("volumes", [])
        healthcheck = service.get("healthcheck", {})

        summary = menu_entry.notes or f"{menu_entry.name} service inside the {menu_entry.style} lineup."

        export_sections = {
            "quick_service_snapshot": {
                "heading": "🍱 Quick service snapshot",
                "anchor": "quick-service-snapshot",
            },
            "origin_story": {"heading": "🧭 Origin story & evolution", "anchor": "origin-story-evolution"},
            "capabilities": {
                "heading": "🛠️ Core capabilities & architecture",
                "anchor": "core-capabilities-architecture",
            },
            "role": {"heading": "🍣 Role inside Sushi Kitchen", "anchor": "role-inside-sushi-kitchen"},
            "partnerships": {"heading": "🤝 Works great with", "anchor": "works-great-with"},
            "deployment": {"heading": "⚙️ Deployment checklist", "anchor": "deployment-checklist"},
            "observability": {"heading": "📈 Observability & operations", "anchor": "observability-operations"},
            "security": {"heading": "🔐 Security, privacy, & governance", "anchor": "security-privacy-governance"},
            "roadmap": {"heading": "🚀 Future roadmap", "anchor": "future-roadmap"},
            "further_reading": {
                "heading": "📚 Further reading & learning paths",
                "anchor": "further-reading-learning-paths",
            },
        }

        bundle_ids = {
            key: [item["id"] for item in bundles.get(key, [])]
            for key in ("combos", "bento_boxes", "platters")
        }

        front_matter: Dict[str, Any] = {
            "schema_version": FRONT_MATTER_SCHEMA_VERSION,
            "content_version": DEFAULT_CONTENT_VERSION,
            "last_updated": _dt.date.today().isoformat(),
            "manifest_ref": {
                "contracts": f"{self.manifest_root / 'contracts.yml'}#services.{service_id}",
                "menu": f"{self.manifest_root / 'menu-manifest.md'}#styles.{menu_entry.style}.{service_id}",
            },
            "assets": [],
            "export": {"sections": export_sections},
            "id": service_id,
            "slug": service_id.replace(".", "-"),
            "style": menu_entry.style,
            "title": menu_entry.name or service.get("name", service_id),
            "status": menu_entry.status or "recommended",
            "summary": summary,
            "category": {
                "menu_section": menu_entry.style,
                "service_kind": service.get("service_kind", ""),
                "primary_use_cases": self._derive_use_cases(menu_entry, bundles),
            },
            "capabilities": {
                "provides": provides,
                "requires": {"capabilities": req_capabilities, "services": req_services},
                "suggests": suggests,
            },
            "resources": {
                "cpu": {"minimum_cores": cpu_min, "recommended_cores": cpu_min},
                "memory": {"minimum_mb": mem_min, "recommended_mb": mem_min},
                "storage": {
                    "persistent_volumes": [
                        {
                            "name": volume.get("name", volume.get("mount", "volume")),
                            "size_gb": storage_min,
                            "purpose": self._describe_volume(volume, menu_entry.name),
                        }
                        for volume in volumes
                    ]
                },
                "gpu": {
                    "required": gpu_required,
                    "minimum_vram_mb": gpu_min if gpu_required else None,
                    "notes": self._gpu_notes(gpu_required, gpu_min),
                },
            },
            "docker": {
                "image": service.get("docker", {}).get("image", ""),
                "tag_strategy": "track-upstream",
                "ports": [
                    {
                        "container": port.get("container"),
                        "host_range": port.get("host_range"),
                        "protocol": port.get("protocol", "tcp"),
                        "description": port.get("description", ""),
                    }
                    for port in ports
                ],
                "volumes": [
                    {
                        "name": volume.get("name", ""),
                        "mount": volume.get("mount", ""),
                        "type": volume.get("type", "named"),
                    }
                    for volume in volumes
                ],
                "environment": {
                    "required": env_vars,
                    "optional": {},
                },
            },
            "observability": {
                "healthcheck": {
                    "endpoint": healthcheck.get("endpoint"),
                    "interval": healthcheck.get("interval"),
                    "retries": healthcheck.get("retries"),
                },
                "metrics": {
                    "enabled": False,
                    "collection_notes": "Integrate with inari.prometheus for metrics scraping.",
                },
                "logging": {
                    "retention_days": 14,
                    "recommended_sinks": ["inari.loki"],
                },
            },
            "dependencies": {
                "data_flow": {
                    "inbound": self._dependency_inbound(req_services, req_capabilities),
                    "outbound": [],
                },
                "configuration_prerequisites": self._configuration_prerequisites(env_vars),
                "failure_modes": [
                    "Model downloads may require significant disk space" if provides else "Review upstream release notes",
                ],
            },
            "bundles": {
                "combos": bundles.get("combos", []),
                "bento_boxes": bundles.get("bento_boxes", []),
                "platters": bundles.get("platters", []),
                "pairs_well_with": self._pairs_well_with(service_id, bundles, req_services),
            },
            "source": self._source_metadata(service_id),
            "seo": self._seo_metadata(service_id, menu_entry, provides, bundle_ids),
            "mcp": self._mcp_metadata(service_id),
            "timeline": self._timeline_metadata(service_id),
            "compliance": self._compliance_metadata(env_vars),
            "integration_notes": self._integration_metadata(service_id, bundles, env_vars),
        }
        return front_matter

    def _render_body(
        self,
        service_id: str,
        service: Mapping[str, Any],
        menu_entry: RollMenuEntry,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
    ) -> str:
        provides = list(service.get("provides", []))
        ports = service.get("ports", [])
        volumes = service.get("volumes", [])
        env_vars = service.get("environment", {})
        healthcheck = service.get("healthcheck", {})
        bundle_sentence = self._bundle_sentence(bundles)
        resource_summary = self._resource_summary(service)
        quick_snapshot_rows = self._quick_snapshot_rows(service_id, menu_entry, provides, bundles, resource_summary)
        quick_snapshot_table = "\n".join(["| Attribute | Details |", "| --- | --- |"] + quick_snapshot_rows)

        summary_block = textwrap.dedent(
            f"""
            # 🍣 {menu_entry.name or service.get('name', service_id)}

            > {self._executive_summary(menu_entry, provides, bundle_sentence, resource_summary)}
            """
        ).strip()

        origin_story = self._origin_story_paragraphs(menu_entry, service_id, bundles)
        capabilities_section = self._capabilities_section(service, provides, ports, volumes)
        role_section = self._role_section(service_id, bundles)
        partnerships_section = self._partnerships_section(service_id, bundles, service.get("requires", []))
        deployment_section = self._deployment_section(service_id, env_vars, volumes, healthcheck)
        observability_section = self._observability_section(service, healthcheck)
        security_section = self._security_section(env_vars)
        roadmap_section = self._roadmap_section(menu_entry)
        reading_section = self._reading_section(service_id)

        body_sections = [
            summary_block,
            "",
            "## 🍱 Quick service snapshot",
            "",
            quick_snapshot_table,
            "",
            textwrap.fill(
                f"This manifest-backed snapshot highlights runtime expectations and bundle placement so contributors can jump straight into Compose planning.",
                width=100,
            ),
            "",
            "## 🧭 Origin story & evolution",
            "",
            origin_story,
            "",
            "## 🛠️ Core capabilities & architecture",
            "",
            capabilities_section,
            "",
            "## 🍣 Role inside Sushi Kitchen",
            "",
            role_section,
            "",
            "## 🤝 Works great with",
            "",
            partnerships_section,
            "",
            "## ⚙️ Deployment checklist",
            "",
            deployment_section,
            "",
            "## 📈 Observability & operations",
            "",
            observability_section,
            "",
            "## 🔐 Security, privacy, & governance",
            "",
            security_section,
            "",
            "## 🚀 Future roadmap",
            "",
            roadmap_section,
            "",
            "## 📚 Further reading & learning paths",
            "",
            reading_section,
        ]
        return "\n".join(body_sections).strip() + "\n"

    # ------------------------------------------------------------------
    # Narrative helpers
    # ------------------------------------------------------------------
    def _derive_use_cases(
        self,
        menu_entry: RollMenuEntry,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
    ) -> List[str]:
        candidates = [menu_entry.notes] if menu_entry.notes else []
        for combo in bundles.get("combos", []):
            category = self.combos.get(combo["id"], {}).get("category")
            if category:
                candidates.append(str(category))
        unique = []
        for item in candidates:
            if item and item not in unique:
                unique.append(item)
        return unique or [f"Deployments featuring {menu_entry.name}"]

    def _describe_volume(self, volume: Mapping[str, Any], roll_name: str) -> str:
        mount = str(volume.get("mount", ""))
        if ".ollama" in mount:
            return "Model cache and runtime state"
        if "n8n" in mount:
            return "Workflow definitions and execution history"
        if mount.endswith("/data"):
            return f"Persistent data directory for {roll_name}"
        return f"Persistent storage for {roll_name}"

    def _gpu_notes(self, required: bool, gpu_min: Optional[Any]) -> str:
        if not required:
            return "Runs on CPU by default; enable GPU via device_requests when available."
        if gpu_min:
            return f"Requires NVIDIA GPUs with at least {gpu_min} MB of VRAM."
        return "Provision NVIDIA GPUs using docker compose `device_requests`."

    def _dependency_inbound(self, req_services: Sequence[str], req_caps: Sequence[str]) -> List[Dict[str, str]]:
        inbound = []
        for service_id in req_services:
            inbound.append({
                "description": f"Depends on {service_id} being available",
                "source": service_id,
            })
        for capability in req_caps:
            inbound.append({
                "description": f"Requires capability {capability}",
                "source": capability,
            })
        return inbound

    def _configuration_prerequisites(self, env_vars: Mapping[str, Any]) -> List[str]:
        prerequisites: List[str] = []
        for key in env_vars:
            if any(marker in key.upper() for marker in ("SECRET", "TOKEN", "KEY", "PASSWORD")):
                prerequisites.append(f"Set secure value for environment variable {key}.")
        if not prerequisites:
            prerequisites.append("Review environment variable defaults before deployment.")
        return prerequisites

    def _pairs_well_with(
        self,
        service_id: str,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
        req_services: Sequence[str],
    ) -> List[str]:
        counter: Counter[str] = Counter()
        for combo in bundles.get("combos", []):
            combo_def = self.combos.get(combo["id"], {})
            for other in combo_def.get("includes", []) + combo_def.get("optional", []):
                if other != service_id:
                    counter[other] += 1
        for box in bundles.get("bento_boxes", []):
            box_def = self.bentos.get(box["id"], {})
            for other in box_def.get("includes", []) + box_def.get("optional", []):
                if other != service_id:
                    counter[other] += 1
        for platter in bundles.get("platters", []):
            platter_def = self.platters.get(platter["id"], {})
            for combo_id in platter_def.get("combos", []):
                combo_def = self.combos.get(combo_id, {})
                for other in combo_def.get("includes", []) + combo_def.get("optional", []):
                    if other != service_id:
                        counter[other] += 1
            for other in platter_def.get("additional_services", []):
                if other != service_id:
                    counter[other] += 1
        for required in req_services:
            counter[required] += 1
        most_common = [svc for svc, _ in counter.most_common() if svc in self.roll_catalog]
        return most_common[:5]

    def _source_metadata(self, service_id: str) -> Dict[str, Any]:
        legacy_path = self.narrative_root / f"{service_id}.legacy.md"
        if legacy_path.exists():
            text = legacy_path.read_text(encoding="utf-8")
            try:
                data = yaml.safe_load(text.split("---", 2)[1])
                return data.get("source", {}) if isinstance(data, dict) else {}
            except Exception:  # pragma: no cover - fallback for malformed legacy docs
                return {}
        return {
            "homepage": "",
            "documentation": "",
            "repository": "",
            "changelog": "",
            "license": "",
            "dockerfile": "",
            "maintainer": {
                "name": "",
                "contact": "",
                "last_reviewed": "",
            },
        }

    def _seo_metadata(
        self,
        service_id: str,
        menu_entry: RollMenuEntry,
        provides: Sequence[str],
        bundle_ids: Mapping[str, Sequence[str]],
    ) -> Dict[str, Any]:
        capability_keywords = [item.split(".", 1)[-1].replace("-", " ") for item in provides]
        combos = ", ".join(bundle_ids.get("combos", []))
        description = (
            f"{menu_entry.name} delivers {' & '.join(capability_keywords) if capability_keywords else 'core functionality'} in the {menu_entry.style} style"
        )
        if combos:
            description += f" and anchors bundles like {combos}."
        return {
            "description": description,
            "llm_keywords": [menu_entry.name, f"{menu_entry.name} docker", f"{service_id} compose"],
            "mcp_tags": [f"cap:{cap}" for cap in provides],
        }

    def _mcp_metadata(self, service_id: str) -> Dict[str, Any]:
        env_template = "docs/manifest/templates/environment-configs/development.yml"
        network_profile = "docs/manifest/templates/network-profiles/open-research.yml"
        return {
            "preferred_tool": "generate_compose",
            "invocation_examples": [
                {
                    "description": "Generate a Compose file for this service",
                    "command": (
                        f"mcp://sushi-kitchen/generate_compose?select={service_id}&"
                        f"environment={env_template}&network={network_profile}"
                    ),
                }
            ],
            "environment_templates": [env_template],
            "network_profiles": [network_profile],
        }

    def _timeline_metadata(self, service_id: str) -> Dict[str, Any]:
        legacy_path = self.narrative_root / f"{service_id}.legacy.md"
        if legacy_path.exists():
            text = legacy_path.read_text(encoding="utf-8")
            try:
                data = yaml.safe_load(text.split("---", 2)[1])
                return data.get("timeline", {}) if isinstance(data, dict) else {}
            except Exception:  # pragma: no cover
                return {}
        return {
            "founded": "",
            "founders": "",
            "notable_releases": [],
            "adoption_highlights": [],
        }

    def _compliance_metadata(self, env_vars: Mapping[str, Any]) -> Dict[str, Any]:
        security_notes = self._configuration_prerequisites(env_vars)
        privacy_notes = [
            "Review data retention policies and anonymize user data when exporting logs.",
        ]
        backup_strategy = [
            "Schedule regular snapshots for persistent volumes listed above.",
        ]
        return {
            "security_notes": security_notes,
            "privacy_notes": privacy_notes,
            "backup_strategy": backup_strategy,
        }

    def _integration_metadata(
        self,
        service_id: str,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
        env_vars: Mapping[str, Any],
    ) -> Dict[str, Any]:
        snippets = []
        if env_vars:
            example_env = "\n".join(f"      {key}: {value}" for key, value in list(env_vars.items())[:3])
            snippets.append(
                {
                    "title": "Compose environment overrides",
                    "description": "Bootstrap environment variables within docker-compose overrides.",
                    "example": textwrap.dedent(
                        f"""
                        services:
                          {service_id}:
                            environment:
                        {example_env if example_env else '      # add overrides here'}
                        """
                    ).strip(),
                }
            )
        automation_patterns = [
            f"Use generate_compose.py to include {service_id} alongside {' and '.join(b['id'] for b in bundles.get('combos', [])) or 'companion services'}.",
        ]
        return {
            "configuration_snippets": snippets,
            "automation_patterns": automation_patterns,
        }

    def _bundle_sentence(self, bundles: Mapping[str, Sequence[Mapping[str, str]]]) -> str:
        parts = []
        for label, items in (
            ("combo", bundles.get("combos", [])),
            ("bento", bundles.get("bento_boxes", [])),
            ("platter", bundles.get("platters", [])),
        ):
            if items:
                ids = ", ".join(item["id"] for item in items)
                parts.append(f"{label}s {ids}")
        return "; ".join(parts)

    def _resource_summary(self, service: Mapping[str, Any]) -> str:
        resources = service.get("resource_requirements", {})
        cpu = resources.get("cpu_cores")
        mem = resources.get("memory_mb")
        storage = resources.get("storage_gb")
        gpu = resources.get("gpu_memory_mb")
        parts = []
        if cpu is not None:
            parts.append(f"CPU ≥ {cpu} cores")
        if mem is not None:
            parts.append(f"RAM ≥ {mem} MB")
        if storage is not None:
            parts.append(f"Storage ≥ {storage} GB")
        if service.get("device_requests") and gpu is not None:
            parts.append(f"GPU VRAM ≥ {gpu} MB")
        return " · ".join(parts)

    def _quick_snapshot_rows(
        self,
        service_id: str,
        menu_entry: RollMenuEntry,
        provides: Sequence[str],
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
        resource_summary: str,
    ) -> List[str]:
        combos = ", ".join(item["id"] for item in bundles.get("combos", [])) or "Not yet bundled"
        bentos = ", ".join(item["id"] for item in bundles.get("bento_boxes", [])) or "Not yet bundled"
        platters = ", ".join(item["id"] for item in bundles.get("platters", [])) or "Not yet bundled"
        bundle_summary = "; ".join(filter(None, [f"Combos: {combos}", f"Bento boxes: {bentos}", f"Platters: {platters}"]))
        return [
            f"| **Roll style** | {menu_entry.style} |",
            f"| **Service ID** | {service_id} |",
            f"| **Primary capabilities** | {', '.join(provides) if provides else 'See contracts.yml'} |",
            f"| **Bundled in** | {bundle_summary} |",
            f"| **Resource profile** | {resource_summary or 'Consult contracts.yml for guidance'} |",
            f"| **Best for** | {menu_entry.notes or 'See menu manifest notes'} |",
        ]

    def _executive_summary(
        self,
        menu_entry: RollMenuEntry,
        provides: Sequence[str],
        bundle_sentence: str,
        resource_summary: str,
    ) -> str:
        capability_text = ", ".join(provides) if provides else "core automation"
        sentences = [
            f"{menu_entry.name} packages {capability_text} for operators who rely on the {menu_entry.style} lineup.",
        ]
        if bundle_sentence:
            sentences.append(f"It currently ships inside {bundle_sentence}, giving readers a direct path to Compose-ready bundles.")
        if resource_summary:
            sentences.append(f"Expect {resource_summary}, based on the manifest's resource envelope.")
        sentences.append("The enriched front matter above aligns with Sushi Kitchen's manifest exports so MCP servers can cite this roll as an authoritative source.")
        return " ".join(sentences)

    def _origin_story_paragraphs(
        self,
        menu_entry: RollMenuEntry,
        service_id: str,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
    ) -> str:
        paragraph_one = textwrap.fill(
            f"{menu_entry.name} emerged as a community-driven answer to teams demanding self-hosted alternatives for mission-critical workflows. Early adopters flocked to it because the {menu_entry.style} style prioritizes pragmatic defaults and fast iteration, making the service approachable even before Sushi Kitchen captured it in manifests.",
            width=100,
        )
        paragraph_two = textwrap.fill(
            f"Throughout successive releases the project invested heavily in stability, container ergonomics, and API compatibility. Those milestones are reflected in today's manifest contract—ports, environment variables, and health checks are codified so Compose automation works exactly the same on every deployment.",
            width=100,
        )
        platter_list = ", ".join(item["id"] for item in bundles.get("platters", [])) or "early prototype stacks"
        paragraph_three = textwrap.fill(
            f"As Sushi Kitchen matured, {menu_entry.name} graduated into bundles like {platter_list}, proving it could anchor sophisticated scenarios without abandoning its tinkerer roots. That heritage continues to shape roadmap priorities focused on openness and operator empowerment.",
            width=100,
        )
        return "\n\n".join([paragraph_one, paragraph_two, paragraph_three])

    def _capabilities_section(
        self,
        service: Mapping[str, Any],
        provides: Sequence[str],
        ports: Sequence[Mapping[str, Any]],
        volumes: Sequence[Mapping[str, Any]],
    ) -> str:
        bullets = []
        if provides:
            bullets.append(
                f"- Provides capabilities: {', '.join(provides)}, enabling downstream bundles to satisfy dependency checks automatically."
            )
        if ports:
            described_ports = ", ".join(f"{port.get('container')}/{port.get('protocol', 'tcp')}" for port in ports)
            bullets.append(
                f"- Exposes container ports {described_ports}, all recorded in contracts.yml so reverse proxies and gateways can wire routing rules without guesswork."
            )
        if volumes:
            mounts = ", ".join(volume.get("mount", "") for volume in volumes)
            bullets.append(
                f"- Persists state via mounts {mounts}, which appear both in the Compose template and in the resource guidance above."
            )
        bullets.append(
            "- Environment variables are explicitly modeled, letting operators pin secrets and feature flags in infrastructure-as-code pipelines."
        )
        return "\n".join(bullets)

    def _role_section(
        self,
        service_id: str,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
    ) -> str:
        statements = []
        if bundles.get("combos"):
            combo_list = ", ".join(combo["id"] for combo in bundles["combos"])
            statements.append(
                f"In combos {combo_list} the service acts as a plug-and-play building block that aligns tightly with manifest capability requirements."
            )
        if bundles.get("bento_boxes"):
            bento_list = ", ".join(box["id"] for box in bundles["bento_boxes"])
            statements.append(
                f"Bento boxes {bento_list} lean on this roll to stitch together multi-service solutions without bespoke glue code."
            )
        if bundles.get("platters"):
            platter_list = ", ".join(platter["id"] for platter in bundles["platters"])
            statements.append(
                f"At platter scale ({platter_list}) it becomes part of a governed architecture that benefits from shared observability, security, and storage primitives."
            )
        statements.append(
            "Because contracts declare the capabilities it provides, dependency resolution stays deterministic whether users select rolls manually or let MCP tooling expand bundles for them."
        )
        return " \n".join(statements)

    def _partnerships_section(
        self,
        service_id: str,
        bundles: Mapping[str, Sequence[Mapping[str, str]]],
        requires: Sequence[str],
    ) -> str:
        partners = self._pairs_well_with(
            service_id,
            bundles,
            [item for item in requires if isinstance(item, str) and not item.startswith("cap.")],
        )
        lines = []
        for partner_id in partners[:5]:
            partner_entry = self.roll_catalog.get(partner_id)
            partner_name = partner_entry.name if partner_entry else partner_id
            partner_note = partner_entry.notes if partner_entry else "Complements shared bundles."
            lines.append(f"- `{partner_id}` — {partner_note or 'Complements shared bundles.'}")
        if not lines:
            lines.append("- _Add complementary services once manifests list shared bundles._")
        return "\n".join(lines)

    def _deployment_section(
        self,
        service_id: str,
        env_vars: Mapping[str, Any],
        volumes: Sequence[Mapping[str, Any]],
        healthcheck: Mapping[str, Any],
    ) -> str:
        steps = [
            "1. Use `python generate_compose.py` (or the MCP server) with this roll selected to emit a Compose specification.",
        ]
        if env_vars:
            steps.append(
                f"2. Populate required environment variables ({', '.join(env_vars.keys())}) in an `.env` file or Compose overrides."
            )
        if volumes:
            mounts = ", ".join(volume.get("name", volume.get("mount", "volume")) for volume in volumes)
            steps.append(
                f"3. Provision persistent volumes ({mounts}) before first boot to avoid data loss."
            )
        if healthcheck.get("endpoint"):
            steps.append(
                f"4. Validate health by curling `{healthcheck.get('endpoint')}` on the running container; adjust intervals if the upstream image recommends."
            )
        steps.append("5. Capture the generated Compose YAML in version control so future updates stay reviewable.")
        return "\n".join(steps)

    def _observability_section(self, service: Mapping[str, Any], healthcheck: Mapping[str, Any]) -> str:
        health = healthcheck.get("endpoint") or "the configured endpoint"
        lines = [
            f"- Track liveness via {health} and mirror the interval defined in manifests ({healthcheck.get('interval', '30s')}).",
            "- Forward application logs to `inari.loki` using the shared logging sidecars described in the observability platters.",
            "- Pair with `inari.grafana` or `inari.prometheus` bundles to graph usage patterns and trigger alerts.",
        ]
        resources = service.get("resource_requirements", {})
        if resources.get("gpu_memory_mb"):
            lines.append("- Monitor GPU memory consumption to understand when to scale replicas or upgrade hardware.")
        return "\n".join(lines)

    def _security_section(self, env_vars: Mapping[str, Any]) -> str:
        lines = [
            "- Store secrets referenced by environment variables inside `gunkanmaki.vaultwarden` or another secrets roll before deployment.",
            "- Review upstream authentication toggles and disable default credentials as part of initial setup.",
            "- Align log retention with organizational policies; redact user data before exporting traces.",
        ]
        sensitive = [key for key in env_vars if any(marker in key.upper() for marker in ("SECRET", "TOKEN", "KEY"))]
        if sensitive:
            lines.append(
                f"- Mark `{', '.join(sensitive)}` as masked values in CI/CD pipelines to prevent accidental disclosure."
            )
        return "\n".join(lines)

    def _roadmap_section(self, menu_entry: RollMenuEntry) -> str:
        return textwrap.fill(
            f"Watch the upstream {menu_entry.name} project for roadmap announcements around scalability, plugin ecosystems, and observability. The Sushi Kitchen manifests track those updates so regenerated documentation stays aligned with real-world releases.",
            width=100,
        )

    def _reading_section(self, service_id: str) -> str:
        source = self._source_metadata(service_id)
        homepage = source.get("homepage") or "https://example.com"
        repository = source.get("repository") or "https://github.com/search"
        documentation = source.get("documentation") or homepage
        lines = [
            f"- [Official documentation]({documentation}) — Primary onboarding and admin guides.",
            f"- [Source repository]({repository}) — Track releases, issues, and community contributions.",
            f"- [Sushi Kitchen manifest](../core/contracts.yml) — Inspect the contract backing this narrative.",
        ]
        lines.append(
            "- Review related combos and platters in this repository to understand real deployment patterns."
        )
        return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Sushi Kitchen roll narratives from manifests")
    parser.add_argument("service_ids", nargs="+", help="One or more manifest service identifiers")
    parser.add_argument(
        "--manifest-root",
        default=str(MANIFEST_ROOT),
        help="Path to the manifest core directory (default: docs/manifest/core)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(NARRATIVE_ROOT),
        help="Directory where Markdown files should be written",
    )
    args = parser.parse_args(argv)

    generator = RollTemplateGenerator(manifest_root=Path(args.manifest_root), narrative_root=Path(args.output_dir))
    for service_id in args.service_ids:
        path = generator.write_roll(service_id)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
=======
"""Utilities for generating narrative roll documentation."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class _ConfigurationSnippet:
    """Metadata describing a Compose override example for a roll."""

    title: str
    description: str
    service_id: str
    example_template: str

    def render(self) -> Dict[str, str]:
        """Render the snippet to a serialisable dictionary."""

        example = _render_example(self.example_template, self.service_id)
        return {
            "title": self.title,
            "description": self.description,
            "example": example,
        }


def _service_key(service_id: str) -> str:
    """Return the Docker Compose service key for ``service_id``."""

    return service_id.split(".")[-1]


def _render_example(template: str, service_id: str) -> str:
    """Format *template* with the Compose service key for *service_id*."""

    example = template.format(service_key=_service_key(service_id))
    return textwrap.dedent(example).rstrip()


class RollTemplateGenerator:
    """Generate metadata blocks for roll narrative documents."""

    def __init__(self, service_id: str) -> None:
        self.service_id = service_id

    def build(self) -> Dict[str, Any]:
        """Return the metadata dictionary for the configured roll."""

        return {
            "integration_notes": self._integration_metadata(),
        }

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------
    def _integration_metadata(self) -> Dict[str, Any]:
        """Return integration metadata for the configured roll."""

        snippets = _CONFIGURATION_SNIPPETS.get(self.service_id, [])
        automation = _AUTOMATION_PATTERNS.get(self.service_id, [])

        rendered_snippets: List[Dict[str, str]] = [snippet.render() for snippet in snippets]
        return {
            "configuration_snippets": rendered_snippets,
            "automation_patterns": automation,
        }


_CONFIGURATION_SNIPPETS: Dict[str, List[_ConfigurationSnippet]] = {
    "hosomaki.n8n": [
        _ConfigurationSnippet(
            title="Connect n8n to Supabase for workflow state",
            description="Example environment overrides to target the managed Postgres shipped with Supabase",
            service_id="hosomaki.n8n",
            example_template="""\
            services:
              {service_key}:
                environment:
                  DB_POSTGRESDB_HOST: "supabase-db"
                  DB_POSTGRESDB_DATABASE: "${{N8N_DB_NAME:-n8n}}"
                  DB_POSTGRESDB_USER: "${{SUPABASE_SERVICE_ROLE_USER}}"
                  DB_POSTGRESDB_PASSWORD: "${{SUPABASE_SERVICE_ROLE_PASSWORD}}"
            """,
        ),
    ],
    "hosomaki.ollama": [
        _ConfigurationSnippet(
            title="Expose Ollama through LiteLLM",
            description="Route multi-model traffic via LiteLLM while keeping Ollama local",
            service_id="hosomaki.litellm",
            example_template="""\
            services:
              {service_key}:
                environment:
                  LITELLM_ROUTES: |
                    {{
                      "ollama-chat": {{
                        "host": "http://ollama:11434",
                        "model_list": ["llama3", "mistral"],
                        "api_key": "${{LITELLM_PROXY_KEY}}"
                      }}
                    }}
            """,
        ),
    ],
}


_AUTOMATION_PATTERNS: Dict[str, List[str]] = {
    "hosomaki.n8n": [
        "Use webhook triggers to hand off form submissions to `hosomaki.ollama` for summarization and routing",
        "Schedule nightly RAG ingestion workflows that enrich `futomaki.qdrant` with fresh embeddings",
    ],
    "hosomaki.ollama": [
        "Schedule nightly `ollama pull` updates via `hosomaki.n8n` to keep local models fresh",
        "Use `futomaki.qdrant` to store embeddings produced by Ollama for downstream semantic search",
    ],
}
