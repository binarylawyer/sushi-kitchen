#!/usr/bin/env python3
"""Generate Docker Compose definitions from Sushi Kitchen manifests.

This module reads the manifest files that describe individual services
(contracts), curated bundles (combos, bento boxes, platters), and
supporting templates for environment configuration and network
profiles.  Given a list of selected service or bundle identifiers, it
resolves dependencies and produces a Docker Compose specification.

The implementation focuses on being faithful to the manifest data model
rather than covering every possible Docker Compose option.  It is meant
as a foundation that other tools (CLI, API, UI) can build upon.
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import yaml


def load_yaml(path: Path) -> Any:
    """Load YAML from *path* and return the parsed structure."""
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _stringify_env_value(value: Any) -> str:
    """Convert *value* to a string suitable for environment variables."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class ManifestResolver:
    """Resolve manifests into a Docker Compose specification."""

    def __init__(
        self,
        contracts: Dict[str, Any],
        combos: Dict[str, Any],
        bento: Dict[str, Any],
        platters: Dict[str, Any],
        env_template: Dict[str, Any],
        network_profile: Dict[str, Any],
    ) -> None:
        self.services: Dict[str, Dict[str, Any]] = contracts.get("services", {})
        self.combos: Dict[str, Dict[str, Any]] = {
            combo["id"]: combo for combo in combos.get("combos", [])
        }
        self.bentos: Dict[str, Dict[str, Any]] = {
            box["id"]: box for box in bento.get("bento_boxes", [])
        }
        self.platters: Dict[str, Dict[str, Any]] = {
            platter["id"]: platter for platter in platters.get("platters", [])
        }

        capabilities = contracts.get("capabilities", {})
        self.capability_providers: Dict[str, List[str]] = {
            cap_id: list(cap_data.get("providers", []))
            for cap_id, cap_data in capabilities.items()
        }
        dependency_resolution = contracts.get("dependency_resolution", {})
        self.default_providers: Dict[str, str] = dependency_resolution.get(
            "default_providers", {}
        )

        self.env_template = env_template or {}
        self.network_profile = network_profile or {}
        self.available_networks: Set[str] = set(
            self.network_profile.get("networks", {}).keys()
        )
        self.global_environment = self._load_global_environment()
        self.service_env_overrides = self._load_service_overrides()

    # ------------------------------------------------------------------
    # Manifest resolution helpers
    # ------------------------------------------------------------------
    def _expand_bundle(self, bundle_id: str) -> List[str]:
        """Expand a bundle (combo, bento, platter) into service IDs."""
        if bundle_id in self.combos:
            combo = self.combos[bundle_id]
            items = list(combo.get("includes", [])) + list(combo.get("optional", []))
        elif bundle_id in self.bentos:
            box = self.bentos[bundle_id]
            items = list(box.get("includes", [])) + list(box.get("optional", []))
        elif bundle_id in self.platters:
            platter = self.platters[bundle_id]
            items = list(platter.get("combos", [])) + list(
                platter.get("additional_services", [])
            )
        else:
            return [bundle_id]

        expanded: List[str] = []
        for item in items:
            if item in self.services:
                expanded.append(item)
            else:
                expanded.extend(self._expand_bundle(item))
        return expanded

    def resolve_services(self, selected: Sequence[str]) -> List[str]:
        """Resolve *selected* IDs (services or bundles) to concrete services."""
        if not selected:
            raise ValueError("No services or bundles were selected")

        resolved: Set[str] = set()
        queue: List[str] = list(selected)
        while queue:
            current = queue.pop()
            if current in self.combos or current in self.bentos or current in self.platters:
                queue.extend(self._expand_bundle(current))
                continue

            if current not in self.services:
                raise ValueError(f"Unknown service or bundle ID: {current}")

            if current in resolved:
                continue

            resolved.add(current)
            service = self.services[current]
            for requirement in service.get("requires", []) or []:
                if requirement in self.services:
                    queue.append(requirement)
                elif requirement.startswith("cap."):
                    provider = self._select_capability_provider(requirement)
                    if provider is None:
                        raise ValueError(
                            f"No provider found for capability '{requirement}' required by '{current}'"
                        )
                    queue.append(provider)
                else:
                    raise ValueError(
                        f"Requirement '{requirement}' referenced by '{current}' does not match a service ID or capability"
                    )
        return sorted(resolved)

    def _select_capability_provider(self, capability: str) -> Optional[str]:
        """Return the preferred provider for *capability* if available."""
        preferred = self.default_providers.get(capability)
        if preferred and preferred in self.services:
            return preferred
        for candidate in self.capability_providers.get(capability, []):
            if candidate in self.services:
                return candidate
        return None

    # ------------------------------------------------------------------
    # Environment handling
    # ------------------------------------------------------------------
    def _load_global_environment(self) -> Dict[str, str]:
        keys = ("global_environment", "environment_overrides", "global_env")
        merged: Dict[str, str] = {}
        for key in keys:
            data = self.env_template.get(key)
            if isinstance(data, dict):
                for env_key, env_value in data.items():
                    merged[env_key] = _stringify_env_value(env_value)
        return merged

    def _load_service_overrides(self) -> Dict[str, Dict[str, str]]:
        overrides: Dict[str, Dict[str, str]] = {}
        raw = self.env_template.get("service_overrides", {})

        def _walk(node: Any) -> None:
            if not isinstance(node, dict):
                return
            for key, value in node.items():
                if isinstance(value, dict) and "." in key:
                    overrides[key] = {
                        env_key: _stringify_env_value(env_value)
                        for env_key, env_value in value.items()
                    }
                else:
                    _walk(value)

        _walk(raw)
        return overrides

    def apply_environment(self, service_id: str, compose_service: Dict[str, Any]) -> None:
        """Merge environment overrides into *compose_service*."""
        environment: Dict[str, str] = {}
        base_env = compose_service.get("environment")
        if isinstance(base_env, dict):
            environment.update({k: _stringify_env_value(v) for k, v in base_env.items()})
        elif isinstance(base_env, list):
            for entry in base_env:
                if isinstance(entry, str) and "=" in entry:
                    key, value = entry.split("=", 1)
                    environment[key] = value
        if self.global_environment:
            environment.update(self.global_environment)
        if service_id in self.service_env_overrides:
            environment.update(self.service_env_overrides[service_id])
        if environment:
            compose_service["environment"] = environment
        elif "environment" in compose_service:
            compose_service.pop("environment")

    # ------------------------------------------------------------------
    # Network handling
    # ------------------------------------------------------------------
    def apply_networks(
        self, service_contract: Dict[str, Any], compose_service: Dict[str, Any]
    ) -> None:
        networks: List[str] = []
        contract_networks = service_contract.get("networks")
        if isinstance(contract_networks, dict):
            for values in contract_networks.values():
                if isinstance(values, Iterable) and not isinstance(values, (str, bytes)):
                    for network in values:
                        if network in self.available_networks and network not in networks:
                            networks.append(network)
        if not networks and self.available_networks:
            networks.append(next(iter(self.available_networks)))
        if networks:
            compose_service["networks"] = networks

    # ------------------------------------------------------------------
    # Compose service construction
    # ------------------------------------------------------------------
    def build_compose(self, selected_ids: Sequence[str]) -> Dict[str, Any]:
        service_ids = self.resolve_services(selected_ids)
        compose: Dict[str, Any] = {"version": "3.9", "services": {}}

        networks = self.network_profile.get("networks")
        if isinstance(networks, dict) and networks:
            compose["networks"] = copy.deepcopy(networks)

        named_volumes: Dict[str, Dict[str, Any]] = {}
        for service_id in service_ids:
            service_contract = self.services[service_id]
            compose_service, discovered_volumes = self._build_service(service_id, service_contract)
            self.apply_environment(service_id, compose_service)
            self.apply_networks(service_contract, compose_service)
            self._apply_resources(service_contract, compose_service)
            self._apply_healthcheck(service_contract, compose_service)
            if discovered_volumes:
                for volume_name in discovered_volumes:
                    named_volumes.setdefault(volume_name, {})
            service_name = service_id.split(".")[-1]
            compose["services"][service_name] = compose_service

        if named_volumes:
            compose["volumes"] = named_volumes
        return compose

    def _build_service(
        self, service_id: str, service_contract: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Set[str]]:
        compose_service: Dict[str, Any] = {}
        named_volumes: Set[str] = set()

        docker_cfg = service_contract.get("docker", {})
        if isinstance(docker_cfg, dict):
            image = docker_cfg.get("image")
            if image:
                compose_service["image"] = image
            platform = docker_cfg.get("platform")
            if platform:
                compose_service["platform"] = platform
            profiles = docker_cfg.get("profiles")
            if profiles:
                compose_service["profiles"] = profiles

        environment = service_contract.get("environment")
        if environment is not None:
            if isinstance(environment, dict):
                compose_service["environment"] = {
                    key: _stringify_env_value(value)
                    for key, value in environment.items()
                }
            elif isinstance(environment, list):
                compose_service["environment"] = list(environment)

        ports = self._convert_ports(service_contract.get("ports"))
        if ports:
            compose_service["ports"] = ports

        volumes, volume_names = self._convert_volumes(service_contract.get("volumes"))
        if volumes:
            compose_service["volumes"] = volumes
            named_volumes.update(volume_names)

        command = service_contract.get("command")
        if command:
            compose_service["command"] = command

        compose_service["restart"] = "unless-stopped"

        return compose_service, named_volumes

    def _convert_ports(self, ports: Optional[Iterable[Any]]) -> List[str]:
        result: List[str] = []
        if not ports:
            return result
        for port in ports:
            if isinstance(port, dict):
                container = port.get("container")
                host = port.get("host") or port.get("host_range")
                protocol = port.get("protocol")
                if not container:
                    continue
                mapping = f"{host}:{container}" if host else str(container)
                if protocol and protocol.lower() != "tcp":
                    mapping = f"{mapping}/{protocol}"
                result.append(mapping)
            else:
                result.append(str(port))
        return result

    def _convert_volumes(
        self, volumes: Optional[Iterable[Any]]
    ) -> Tuple[List[str], Set[str]]:
        result: List[str] = []
        named: Set[str] = set()
        if not volumes:
            return result, named
        for volume in volumes:
            if isinstance(volume, str):
                result.append(volume)
                name = volume.split(":", 1)[0]
                if name and "/" not in name:
                    named.add(name)
                continue
            if not isinstance(volume, dict):
                continue
            mount = volume.get("mount") or volume.get("target")
            if not mount:
                continue
            vol_type = (volume.get("type") or "named").lower()
            if vol_type == "bind":
                source = volume.get("source")
                if source:
                    result.append(f"{source}:{mount}")
            else:
                name = volume.get("name") or volume.get("source")
                if name:
                    result.append(f"{name}:{mount}")
                    named.add(name)
        return result, named

    def _apply_resources(
        self, service_contract: Dict[str, Any], compose_service: Dict[str, Any]
    ) -> None:
        requirements = service_contract.get("resource_requirements", {})
        if not isinstance(requirements, dict):
            requirements = {}
        deploy: Dict[str, Any] = {}
        limits: Dict[str, Any] = {}
        reservations: Dict[str, Any] = {}

        cpu = requirements.get("cpu_cores")
        if cpu is not None:
            cpu_str = str(cpu)
            limits["cpus"] = cpu_str
            reservations["cpus"] = cpu_str

        memory_mb = requirements.get("memory_mb")
        if memory_mb is not None:
            memory_str = f"{int(memory_mb)}M"
            limits["memory"] = memory_str
            reservations["memory"] = memory_str

        if limits or reservations:
            resources: Dict[str, Any] = {}
            if limits:
                resources["limits"] = limits
            if reservations:
                resources["reservations"] = reservations
            deploy["resources"] = resources

        device_requests = service_contract.get("device_requests")
        if isinstance(device_requests, list) and device_requests:
            resources = deploy.setdefault("resources", {})
            reservations = resources.setdefault("reservations", {})
            devices: List[Dict[str, Any]] = []
            for request in device_requests:
                if not isinstance(request, dict):
                    continue
                device_entry: Dict[str, Any] = {}
                driver = request.get("driver")
                if driver:
                    device_entry["driver"] = driver
                count = request.get("count")
                if count is not None:
                    try:
                        device_entry["count"] = int(count)
                    except (TypeError, ValueError):
                        # Docker Compose expects an integer count; skip non-numeric values.
                        pass
                capabilities = request.get("capabilities")
                if capabilities:
                    device_entry["capabilities"] = capabilities
                if device_entry:
                    devices.append(device_entry)
            if devices:
                reservations["devices"] = devices

        if deploy:
            compose_service["deploy"] = deploy

    def _apply_healthcheck(
        self, service_contract: Dict[str, Any], compose_service: Dict[str, Any]
    ) -> None:
        health = service_contract.get("healthcheck")
        if not isinstance(health, dict) or not health:
            return
        healthcheck: Dict[str, Any] = {}
        if "command" in health:
            healthcheck["test"] = health["command"]
        elif "endpoint" in health:
            endpoint = str(health.get("endpoint"))
            port = self._guess_primary_port(service_contract)
            url = f"http://localhost:{port}{endpoint}" if port else endpoint
            healthcheck["test"] = ["CMD-SHELL", f"curl -f {url}"]
        for key in ("interval", "timeout", "retries", "start_period"):
            if key in health:
                healthcheck[key] = health[key]
        if healthcheck:
            compose_service["healthcheck"] = healthcheck

    def _guess_primary_port(self, service_contract: Dict[str, Any]) -> Optional[int]:
        ports = service_contract.get("ports")
        if not isinstance(ports, list):
            return None
        for port in ports:
            if isinstance(port, dict) and port.get("container"):
                try:
                    return int(str(port["container"]).split("/")[0])
                except ValueError:
                    return None
        return None


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Docker Compose specification from Sushi Kitchen manifests"
    )
    parser.add_argument("--contracts", type=Path, required=True, help="Path to contracts.yml")
    parser.add_argument("--combos", type=Path, required=True, help="Path to combos.yml")
    parser.add_argument("--bento", type=Path, required=True, help="Path to bento-box.yml")
    parser.add_argument("--platters", type=Path, required=True, help="Path to platters.yml")
    parser.add_argument(
        "--environment",
        type=Path,
        required=True,
        help="Environment template to apply (e.g. development.yml)",
    )
    parser.add_argument(
        "--network",
        type=Path,
        required=True,
        help="Network profile to apply (e.g. open-research.yml)",
    )
    parser.add_argument(
        "--select",
        nargs="+",
        default=[],
        help="Service or bundle IDs to include in the generated Compose file",
    )

    args = parser.parse_args(argv)

    contracts_data = load_yaml(args.contracts)
    combos_data = load_yaml(args.combos)
    bento_data = load_yaml(args.bento)
    platters_data = load_yaml(args.platters)
    env_data = load_yaml(args.environment)
    network_data = load_yaml(args.network)

    resolver = ManifestResolver(
        contracts=contracts_data,
        combos=combos_data,
        bento=bento_data,
        platters=platters_data,
        env_template=env_data,
        network_profile=network_data,
    )
    try:
        compose_dict = resolver.build_compose(args.select)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    yaml.safe_dump(compose_dict, sys.stdout, sort_keys=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
