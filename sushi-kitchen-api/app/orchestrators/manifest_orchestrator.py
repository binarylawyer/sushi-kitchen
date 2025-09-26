#!/usr/bin/env python3
"""
Orchestrates calls to core repository scripts.
This is the bridge between FastAPI and the core generation logic.
"""

import asyncio
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import tempfile

class ManifestOrchestrator:
    def __init__(self, core_repo_path: str):
        self.core_path = Path(core_repo_path)
        self.scripts = {
            'compose': self.core_path / 'scripts' / 'generate-compose.py',
            'export': self.core_path / 'scripts' / 'export-manifest-json.py',
            'network': self.core_path / 'scripts' / 'generate-network-config.py'
        }

        # Check if we have a local generated directory (for serving pre-built bundles)
        self.generated_dir = Path('/app/generated')  # Docker mount point
        if not self.generated_dir.exists():
            # Fallback to relative path for development
            self.generated_dir = Path(__file__).parent.parent.parent / 'generated'

    async def generate_complete_stack(
        self,
        selection_type: str,
        selection_id: str,
        profile: str = 'chirashi',
        include_optional: bool = False
    ) -> Dict:
        """
        Complete stack generation:
        1. Generate base compose using existing script
        2. Apply network configuration
        3. Add security overlays
        """

        # Step 1: Generate base compose
        compose_yaml = await self._run_compose_generator(
            selection_type,
            selection_id,
            include_optional
        )

        # Step 2: Apply network configuration
        networked_compose = await self._apply_network_config(
            compose_yaml,
            profile
        )

        # Step 3: Apply security policies
        final_compose = await self._apply_security_policies(
            networked_compose,
            profile
        )

        return final_compose

    async def _run_compose_generator(
        self,
        selection_type: str,
        selection_id: str,
        include_optional: bool
    ) -> str:
        """Execute the existing generate-compose.py script"""

        cmd = [
            'python3',
            str(self.scripts['compose']),
            f'--{selection_type}={selection_id}',
            '--manifest-dir', str(self.core_path / 'docs' / 'manifest')
        ]

        if include_optional:
            cmd.append('--include-optional')

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.core_path)
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"Compose generation failed: {stderr.decode()}")

        return stdout.decode()

    async def _apply_network_config(self, compose_yaml: str, profile: str) -> Dict:
        """Apply network configuration using generate-network-config.py"""

        # Write compose to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as temp_file:
            temp_file.write(compose_yaml)
            temp_compose_path = temp_file.name

        try:
            cmd = [
                'python3',
                str(self.scripts['network']),
                '--compose-file', temp_compose_path,
                '--profile', profile
            ]

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.core_path)
            )

            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                raise RuntimeError(f"Network configuration failed: {stderr.decode()}")

            return yaml.safe_load(stdout.decode())

        finally:
            # Clean up temp file
            Path(temp_compose_path).unlink(missing_ok=True)

    async def _apply_security_policies(self, compose_dict: Dict, profile: str) -> Dict:
        """Apply security policies based on profile"""

        # Add security labels and constraints based on profile
        if profile == 'inari':  # Enterprise
            for service_name, service_config in compose_dict.get('services', {}).items():
                service_config.setdefault('security_opt', []).extend([
                    'no-new-privileges:true',
                    'apparmor:docker-default'
                ])
                service_config.setdefault('read_only', True)
                service_config.setdefault('cap_drop', ['ALL'])

                # Add tmpfs for writable areas
                if service_name in ['postgres', 'neo4j', 'redis']:
                    service_config.setdefault('tmpfs', []).append('/tmp')

        elif profile == 'temaki':  # Business
            for service_name, service_config in compose_dict.get('services', {}).items():
                service_config.setdefault('security_opt', []).append('no-new-privileges:true')
                service_config.setdefault('cap_drop', ['NET_ADMIN', 'SYS_ADMIN'])

        return compose_dict

    async def get_available_components(self) -> Dict:
        """Get all available platters, combos, and rolls"""

        # First try to load from pre-built bundle if available
        bundle_path = self.generated_dir / 'api-bundle.json'
        if bundle_path.exists():
            try:
                with bundle_path.open() as f:
                    bundle_data = json.load(f)
                return {
                    'platters': bundle_data.get('platters', {}),
                    'combos': bundle_data.get('combos', {}),
                    'rolls': bundle_data.get('services', {}),  # Services are rolls
                    'capabilities': bundle_data.get('capabilities', {}),
                    'network_profiles': bundle_data.get('network_profiles', {})
                }
            except (json.JSONDecodeError, KeyError):
                # Fall back to dynamic generation if bundle is corrupted
                pass

        # Fall back to dynamic generation using export script
        cmd = [
            'python3',
            str(self.scripts['export']),
            '--manifest-root', str(self.core_path / 'docs' / 'manifest'),
            '--output-dir', str(self.core_path / 'tmp' / 'api-export')
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.core_path)
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"Export failed: {stderr.decode()}")

        # Load the generated JSON files
        export_dir = self.core_path / 'tmp' / 'api-export'
        components = {
            'platters': [],
            'combos': [],
            'rolls': {}
        }

        # Load platters
        platters_file = export_dir / 'platters.json'
        if platters_file.exists():
            with platters_file.open() as f:
                components['platters'] = json.load(f).get('platters', [])

        # Load combos
        combos_file = export_dir / 'combos.json'
        if combos_file.exists():
            with combos_file.open() as f:
                components['combos'] = json.load(f).get('combos', [])

        # Load contracts (rolls)
        contracts_file = export_dir / 'contracts.json'
        if contracts_file.exists():
            with contracts_file.open() as f:
                contracts_data = json.load(f)
                components['rolls'] = contracts_data.get('rolls', {})
                components['capabilities'] = contracts_data.get('capabilities', {})

        return components

    async def validate_configuration(self, compose_dict: Dict) -> Dict:
        """Validate the generated configuration"""

        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': []
        }

        # Check for required services
        services = compose_dict.get('services', {})

        # Validate network assignments
        networks = compose_dict.get('networks', {})
        for service_name, service_config in services.items():
            service_networks = service_config.get('networks', [])
            for network in service_networks:
                if network not in networks:
                    validation_results['errors'].append(
                        f"Service '{service_name}' references undefined network '{network}'"
                    )
                    validation_results['valid'] = False

        # Check for port conflicts
        used_ports = set()
        for service_name, service_config in services.items():
            ports = service_config.get('ports', [])
            for port_mapping in ports:
                if isinstance(port_mapping, str) and ':' in port_mapping:
                    host_port = port_mapping.split(':')[0]
                    # Extract port from environment variable format
                    if ':-' in host_port:
                        default_port = host_port.split(':-')[1].rstrip('}')
                        if default_port in used_ports:
                            validation_results['warnings'].append(
                                f"Potential port conflict on {default_port} for service '{service_name}'"
                            )
                        used_ports.add(default_port)

        return validation_results