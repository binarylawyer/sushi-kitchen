#!/usr/bin/env python3
"""
Creates a single JSON bundle for the API from all manifest files.
Run during CI/CD to create a versioned, cacheable bundle.
"""

import json
import yaml
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import argparse

class APIBundleGenerator:
    def __init__(self, manifest_dir: Path):
        self.manifest_dir = manifest_dir
        self.bundle = {
            'version': '1.0.0',
            'generated_at': datetime.utcnow().isoformat(),
            'checksums': {},
            'services': {},
            'combos': {},
            'bentos': {},
            'platters': {},
            'capabilities': {},
            'badges': {},
            'network_profiles': {},
            'security_policies': {}
        }

    def generate(self) -> Dict:
        """Generate complete API bundle"""

        # Load all manifests
        self._load_contracts()
        self._load_combos()
        self._load_bentos()
        self._load_platters()
        self._load_badges()
        self._load_network_profiles()

        # Calculate checksums for verification
        self._calculate_checksums()

        return self.bundle

    def _load_contracts(self):
        """Load and process contracts.yml"""
        contracts_path = self.manifest_dir / 'contracts.yml'
        if not contracts_path.exists():
            return

        with open(contracts_path) as f:
            data = yaml.safe_load(f)

            # Extract services with simplified structure for API
            for service_id, service_data in data.get('services', {}).items():
                self.bundle['services'][service_id] = {
                    'id': service_id,
                    'name': service_data.get('name'),
                    'category': service_id.split('.')[0],
                    'provides': service_data.get('provides', []),
                    'requires': service_data.get('requires', []),
                    'resource_requirements': service_data.get('resource_requirements', {}),
                    'docker': service_data.get('docker', {}),
                    'description': service_data.get('description', ''),
                    'status': service_data.get('status', 'stable')
                }

            self.bundle['capabilities'] = data.get('capabilities', {})

    def _load_combos(self):
        """Load combos.yml"""
        combos_path = self.manifest_dir / 'combos.yml'
        if not combos_path.exists():
            return

        with open(combos_path) as f:
            data = yaml.safe_load(f)

            for combo_data in data.get('combos', []):
                combo_id = combo_data['id']
                self.bundle['combos'][combo_id] = {
                    'id': combo_id,
                    'name': combo_data.get('name', ''),
                    'description': combo_data.get('description', ''),
                    'includes': combo_data.get('includes', []),
                    'optional': combo_data.get('optional', []),
                    'provides': combo_data.get('provides', []),
                    'difficulty': combo_data.get('difficulty', 'intermediate'),
                    'estimated_setup_time_min': combo_data.get('estimated_setup_time_min', 15),
                    'tags': combo_data.get('tags', [])
                }

    def _load_bentos(self):
        """Load bentos.yml (if exists)"""
        bentos_path = self.manifest_dir / 'bentos.yml'
        if not bentos_path.exists():
            return

        with open(bentos_path) as f:
            data = yaml.safe_load(f)

            for bento_data in data.get('bentos', []):
                bento_id = bento_data['id']
                self.bundle['bentos'][bento_id] = {
                    'id': bento_id,
                    'name': bento_data.get('name', ''),
                    'description': bento_data.get('description', ''),
                    'includes': bento_data.get('includes', []),
                    'optional': bento_data.get('optional', []),
                    'provides': bento_data.get('provides', []),
                    'category': bento_data.get('category', 'general'),
                    'tags': bento_data.get('tags', [])
                }

    def _load_platters(self):
        """Load platters.yml"""
        platters_path = self.manifest_dir / 'platters.yml'
        if not platters_path.exists():
            return

        with open(platters_path) as f:
            data = yaml.safe_load(f)

            for platter_data in data.get('platters', []):
                platter_id = platter_data['id']
                self.bundle['platters'][platter_id] = {
                    'id': platter_id,
                    'name': platter_data.get('name', ''),
                    'description': platter_data.get('description', ''),
                    'includes': platter_data.get('includes', []),
                    'optional': platter_data.get('optional', []),
                    'provides': platter_data.get('provides', []),
                    'resource_requirements': platter_data.get('resource_requirements', {}),
                    'difficulty': platter_data.get('difficulty', 'intermediate'),
                    'estimated_setup_time_min': platter_data.get('estimated_setup_time_min', 30),
                    'tags': platter_data.get('tags', [])
                }

    def _load_badges(self):
        """Load badges configuration"""
        badges_path = self.manifest_dir / 'badges.yml'
        if not badges_path.exists():
            # Create default badges
            self.bundle['badges'] = {
                'stability': {
                    'alpha': {'color': '#ff4444', 'label': 'Alpha'},
                    'beta': {'color': '#ff8800', 'label': 'Beta'},
                    'stable': {'color': '#44ff44', 'label': 'Stable'},
                    'deprecated': {'color': '#888888', 'label': 'Deprecated'}
                },
                'difficulty': {
                    'easy': {'color': '#44ff44', 'label': 'Easy'},
                    'intermediate': {'color': '#ffaa00', 'label': 'Intermediate'},
                    'advanced': {'color': '#ff4444', 'label': 'Advanced'}
                }
            }
            return

        with open(badges_path) as f:
            self.bundle['badges'] = yaml.safe_load(f)

    def _load_network_profiles(self):
        """Load network security profiles"""
        self.bundle['network_profiles'] = {
            'chirashi': {
                'name': 'Research/Development',
                'description': 'Single network for research and development use',
                'security_level': 'low',
                'suitable_for': ['development', 'research', 'learning']
            },
            'temaki': {
                'name': 'Business/Production',
                'description': 'Segmented networks for business production use',
                'security_level': 'medium',
                'suitable_for': ['business', 'production', 'small-team']
            },
            'inari': {
                'name': 'Enterprise/Compliance',
                'description': 'Multi-tier isolated networks for enterprise compliance',
                'security_level': 'high',
                'suitable_for': ['enterprise', 'compliance', 'high-security']
            }
        }

        # Load from file if exists
        profiles_path = self.manifest_dir / 'network-profiles.yml'
        if profiles_path.exists():
            with open(profiles_path) as f:
                file_profiles = yaml.safe_load(f)
                self.bundle['network_profiles'].update(file_profiles.get('profiles', {}))

    def _calculate_checksums(self):
        """Calculate checksums for all loaded manifest files"""
        for file_path in self.manifest_dir.glob('*.yml'):
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    content = f.read()
                    sha256_hash = hashlib.sha256(content).hexdigest()
                    self.bundle['checksums'][file_path.name] = sha256_hash

    def save_bundle(self, output_path: Path, pretty: bool = False):
        """Save bundle to JSON file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            if pretty:
                json.dump(self.bundle, f, indent=2, ensure_ascii=False)
                f.write('\n')
            else:
                json.dump(self.bundle, f, separators=(',', ':'), ensure_ascii=False)

    def get_stats(self) -> Dict:
        """Get statistics about the generated bundle"""
        return {
            'services_count': len(self.bundle['services']),
            'combos_count': len(self.bundle['combos']),
            'platters_count': len(self.bundle['platters']),
            'capabilities_count': len(self.bundle['capabilities']),
            'total_size_bytes': len(json.dumps(self.bundle, separators=(',', ':')))
        }

def main():
    parser = argparse.ArgumentParser(description='Generate API bundle from Sushi Kitchen manifests')
    parser.add_argument('--manifest-dir', type=Path, default=Path('docs/manifest'),
                       help='Manifest directory path')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output JSON file path')
    parser.add_argument('--pretty', action='store_true',
                       help='Pretty-print JSON output')
    parser.add_argument('--stats', action='store_true',
                       help='Show bundle statistics')

    args = parser.parse_args()

    if not args.manifest_dir.exists():
        print(f"Error: Manifest directory '{args.manifest_dir}' not found")
        return 1

    # Generate bundle
    generator = APIBundleGenerator(args.manifest_dir)
    bundle = generator.generate()

    # Save bundle
    generator.save_bundle(args.output, args.pretty)
    print(f"API bundle generated: {args.output}")

    # Show stats if requested
    if args.stats:
        stats = generator.get_stats()
        print(f"Bundle Statistics:")
        print(f"  Services: {stats['services_count']}")
        print(f"  Combos: {stats['combos_count']}")
        print(f"  Platters: {stats['platters_count']}")
        print(f"  Capabilities: {stats['capabilities_count']}")
        print(f"  Total Size: {stats['total_size_bytes']:,} bytes")

    return 0

if __name__ == '__main__':
    exit(main())