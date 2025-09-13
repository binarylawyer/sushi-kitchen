#!/usr/bin/env python3
"""
🍣 Sushi Kitchen — Manifest-to-Compose Generator

This script reads the manifest files (platters.yml, combos.yml, contracts.yml)
and generates Docker Compose configurations based on the selected platter.

Usage:
    python scripts/generate-compose.py --platter=platter.starter --output=compose/generated/starter.yml
    python scripts/generate-compose.py --combo=combo.dev-tools --output=compose/generated/dev-tools.yml
    python scripts/generate-compose.py --roll=hosomaki.redis --output=compose/generated/redis.yml
"""

import argparse
import yaml
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass

@dataclass
class Roll:
    """Represents a roll from contracts.yml"""
    id: str
    provides: List[str]
    requires: List[str] = None
    suggests: List[str] = None
    conflicts: List[str] = None
    image: str = ""
    ports: List[Dict] = None
    environment_vars: List[str] = None
    volumes: List[str] = None
    networks: List[str] = None
    depends_on: List[str] = None

@dataclass
class Combo:
    """Represents a combo from combos.yml"""
    id: str
    name: str
    includes: List[str]
    optional: List[str] = None
    provides: List[str] = None

@dataclass
class Platter:
    """Represents a platter from platters.yml"""
    id: str
    name: str
    includes: List[str]
    optional: List[str] = None
    provides: List[str] = None

class ManifestResolver:
    """Resolves dependencies and generates compose configurations"""
    
    def __init__(self, manifest_dir: Path):
        self.manifest_dir = manifest_dir
        self.rolls: Dict[str, Roll] = {}
        self.combos: Dict[str, Combo] = {}
        self.platters: Dict[str, Platter] = {}
        self.capabilities: Dict[str, Dict] = {}
        self.load_manifests()
    
    def load_manifests(self):
        """Load all manifest files"""
        # Load contracts.yml
        contracts_path = self.manifest_dir / "contracts.yml"
        if contracts_path.exists():
            with open(contracts_path, 'r') as f:
                contracts = yaml.safe_load(f)
                self.capabilities = contracts.get('capabilities', {})
                self.load_rolls(contracts.get('rolls', {}))
        
        # Load combos.yml
        combos_path = self.manifest_dir / "combos.yml"
        if combos_path.exists():
            with open(combos_path, 'r') as f:
                combos_data = yaml.safe_load(f)
                self.load_combos(combos_data.get('combos', []))
        
        # Load platters.yml
        platters_path = self.manifest_dir / "platters.yml"
        if platters_path.exists():
            with open(platters_path, 'r') as f:
                platters_data = yaml.safe_load(f)
                self.load_platters(platters_data.get('platters', []))
    
    def load_rolls(self, rolls_data: Dict):
        """Load rolls from contracts.yml"""
        for roll_id, roll_data in rolls_data.items():
            self.rolls[roll_id] = Roll(
                id=roll_id,
                provides=roll_data.get('provides', []),
                requires=roll_data.get('requires', []),
                suggests=roll_data.get('suggests', []),
                conflicts=roll_data.get('conflicts', []),
                image=roll_data.get('image', ''),
                ports=roll_data.get('ports', []),
                environment_vars=roll_data.get('environment_vars', []),
                volumes=roll_data.get('volumes', []),
                networks=roll_data.get('networks', []),
                depends_on=roll_data.get('depends_on', [])
            )
    
    def load_combos(self, combos_data: List[Dict]):
        """Load combos from combos.yml"""
        for combo_data in combos_data:
            combo_id = combo_data['id']
            self.combos[combo_id] = Combo(
                id=combo_id,
                name=combo_data.get('name', ''),
                includes=combo_data.get('includes', []),
                optional=combo_data.get('optional', []),
                provides=combo_data.get('provides', [])
            )
    
    def load_platters(self, platters_data: List[Dict]):
        """Load platters from platters.yml"""
        for platter_data in platters_data:
            platter_id = platter_data['id']
            self.platters[platter_id] = Platter(
                id=platter_id,
                name=platter_data.get('name', ''),
                includes=platter_data.get('includes', []),
                optional=platter_data.get('optional', []),
                provides=platter_data.get('provides', [])
            )
    
    def resolve_platter(self, platter_id: str, include_optional: bool = False) -> Set[str]:
        """Resolve a platter to its constituent rolls"""
        if platter_id not in self.platters:
            raise ValueError(f"Platter '{platter_id}' not found")
        
        platter = self.platters[platter_id]
        required_rolls = set()
        
        # Resolve includes
        for item in platter.includes:
            if item.startswith('combo.'):
                combo_rolls = self.resolve_combo(item)
                required_rolls.update(combo_rolls)
            elif item.startswith('platter.'):
                sub_platter_rolls = self.resolve_platter(item, include_optional)
                required_rolls.update(sub_platter_rolls)
            else:
                required_rolls.add(item)
        
        # Resolve optional if requested
        if include_optional:
            for item in platter.optional:
                if item.startswith('combo.'):
                    combo_rolls = self.resolve_combo(item)
                    required_rolls.update(combo_rolls)
                else:
                    required_rolls.add(item)
        
        return required_rolls
    
    def resolve_combo(self, combo_id: str) -> Set[str]:
        """Resolve a combo to its constituent rolls"""
        if combo_id not in self.combos:
            raise ValueError(f"Combo '{combo_id}' not found")
        
        combo = self.combos[combo_id]
        required_rolls = set()
        
        for roll_id in combo.includes:
            required_rolls.add(roll_id)
        
        return required_rolls
    
    def resolve_dependencies(self, roll_ids: Set[str]) -> Set[str]:
        """Resolve all dependencies for a set of rolls"""
        resolved = set()
        to_resolve = set(roll_ids)
        
        while to_resolve:
            current = to_resolve.pop()
            if current in resolved:
                continue
            
            resolved.add(current)
            
            if current in self.rolls:
                roll = self.rolls[current]
                # Add required rolls
                for req in roll.requires or []:
                    if req.startswith('cap.'):
                        # Find a provider for this capability
                        provider = self.find_capability_provider(req)
                        if provider:
                            to_resolve.add(provider)
                    else:
                        to_resolve.add(req)
                
                # Add suggested rolls
                for sugg in roll.suggests or []:
                    if sugg.startswith('cap.'):
                        provider = self.find_capability_provider(sugg)
                        if provider and provider not in resolved:
                            to_resolve.add(provider)
                    else:
                        to_resolve.add(sugg)
        
        return resolved
    
    def find_capability_provider(self, capability: str) -> Optional[str]:
        """Find a roll that provides a capability"""
        if capability not in self.capabilities:
            return None
        
        providers = self.capabilities[capability].get('providers', [])
        if providers:
            # Return the first available provider
            for provider in providers:
                if provider in self.rolls:
                    return provider
        
        return None
    
    def generate_compose(self, roll_ids: Set[str]) -> Dict:
        """Generate Docker Compose configuration for a set of rolls"""
        compose = {
            'version': '3.9',
            'services': {},
            'volumes': {},
            'networks': {
                'sushi-net': {
                    'driver': 'bridge'
                }
            }
        }
        
        for roll_id in roll_ids:
            if roll_id in self.rolls:
                service_config = self.generate_service_config(roll_id)
                if service_config:
                    service_name = roll_id.split('.')[-1]  # e.g., 'redis' from 'hosomaki.redis'
                    compose['services'][service_name] = service_config
        
        return compose
    
    def generate_service_config(self, roll_id: str) -> Optional[Dict]:
        """Generate service configuration for a roll"""
        if roll_id not in self.rolls:
            return None
        
        roll = self.rolls[roll_id]
        service = {}
        
        # Image
        if roll.image:
            service['image'] = roll.image
        
        # Ports
        if roll.ports:
            service['ports'] = []
            for port_config in roll.ports:
                if isinstance(port_config, dict):
                    container_port = port_config.get('container')
                    host_port = port_config.get('host')
                    if container_port and host_port:
                        service['ports'].append(f"${{{host_port.upper()}_PORT:-{host_port}}}:{container_port}")
                else:
                    service['ports'].append(str(port_config))
        
        # Environment variables
        if roll.environment_vars:
            service['environment'] = []
            for env_var in roll.environment_vars:
                service['environment'].append(f"${{{env_var}}}")
        
        # Volumes
        if roll.volumes:
            service['volumes'] = roll.volumes
        
        # Networks
        service['networks'] = ['sushi-net']
        
        # Dependencies
        if roll.depends_on:
            service['depends_on'] = roll.depends_on
        
        # Restart policy
        service['restart'] = 'unless-stopped'
        
        return service

def main():
    parser = argparse.ArgumentParser(description='Generate Docker Compose from Sushi Kitchen manifests')
    parser.add_argument('--platter', help='Platter ID to generate')
    parser.add_argument('--combo', help='Combo ID to generate')
    parser.add_argument('--roll', help='Single roll ID to generate')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--include-optional', action='store_true', help='Include optional components')
    parser.add_argument('--manifest-dir', default='docs/manifest', help='Manifest directory path')
    
    args = parser.parse_args()
    
    if not any([args.platter, args.combo, args.roll]):
        parser.error('Must specify --platter, --combo, or --roll')
    
    manifest_dir = Path(args.manifest_dir)
    if not manifest_dir.exists():
        print(f"Error: Manifest directory '{manifest_dir}' not found")
        sys.exit(1)
    
    resolver = ManifestResolver(manifest_dir)
    
    try:
        if args.platter:
            roll_ids = resolver.resolve_platter(args.platter, args.include_optional)
            print(f"Resolving platter '{args.platter}' -> {len(roll_ids)} rolls")
        elif args.combo:
            roll_ids = resolver.resolve_combo(args.combo)
            print(f"Resolving combo '{args.combo}' -> {len(roll_ids)} rolls")
        elif args.roll:
            roll_ids = {args.roll}
            print(f"Generating single roll '{args.roll}'")
        
        # Resolve dependencies
        all_rolls = resolver.resolve_dependencies(roll_ids)
        print(f"With dependencies -> {len(all_rolls)} total rolls")
        
        # Generate compose
        compose = resolver.generate_compose(all_rolls)
        
        # Output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
            print(f"Generated compose file: {output_path}")
        else:
            print(yaml.dump(compose, default_flow_style=False, sort_keys=False))
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
