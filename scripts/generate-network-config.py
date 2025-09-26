#!/usr/bin/env python3
"""
Generate network configurations based on privacy profiles.
Extends the base compose with network isolation rules.
"""

import yaml
from pathlib import Path
from typing import Dict, List

class NetworkConfigGenerator:
    def __init__(self):
        self.profiles = {
            'chirashi': self._generate_chirashi_network,
            'temaki': self._generate_temaki_network,
            'inari': self._generate_inari_network
        }

    def generate(self, compose_dict: Dict, profile: str) -> Dict:
        """Apply network profile to existing compose configuration"""
        if profile not in self.profiles:
            raise ValueError(f"Unknown profile: {profile}")

        # Add network definitions
        compose_dict['networks'] = self.profiles[profile]()

        # Update each service with appropriate network assignments
        for service_name, service_config in compose_dict['services'].items():
            service_config['networks'] = self._assign_service_networks(
                service_name,
                service_config,
                profile
            )

        return compose_dict

    def _generate_chirashi_network(self) -> Dict:
        """Single network for research/development"""
        return {
            'sushi_net': {
                'driver': 'bridge',
                'ipam': {
                    'config': [{'subnet': '172.20.0.0/16'}]
                }
            }
        }

    def _generate_temaki_network(self) -> Dict:
        """Segmented networks for business use"""
        return {
            'sushi_frontend': {
                'driver': 'bridge',
                'external': True
            },
            'sushi_backend': {
                'driver': 'bridge',
                'internal': True
            },
            'sushi_data': {
                'driver': 'bridge',
                'internal': True
            }
        }

    def _generate_inari_network(self) -> Dict:
        """Enterprise-grade isolated networks"""
        return {
            'sushi_web_tier': {
                'driver': 'bridge',
                'ipam': {
                    'config': [{'subnet': '172.21.1.0/24'}]
                }
            },
            'sushi_app_tier': {
                'driver': 'bridge',
                'internal': True,
                'ipam': {
                    'config': [{'subnet': '172.21.2.0/24'}]
                }
            },
            'sushi_data_tier': {
                'driver': 'bridge',
                'internal': True,
                'ipam': {
                    'config': [{'subnet': '172.21.3.0/24'}]
                }
            },
            'sushi_mgmt_tier': {
                'driver': 'bridge',
                'internal': True,
                'ipam': {
                    'config': [{'subnet': '172.21.4.0/24'}]
                }
            }
        }

    def _assign_service_networks(self, service_name: str, service_config: Dict, profile: str) -> List[str]:
        """Assign appropriate networks to a service based on profile and service type"""

        if profile == 'chirashi':
            return ['sushi_net']

        elif profile == 'temaki':
            # Business segmentation
            if self._is_web_service(service_name, service_config):
                return ['sushi_frontend', 'sushi_backend']
            elif self._is_data_service(service_name, service_config):
                return ['sushi_data']
            else:
                return ['sushi_backend']

        elif profile == 'inari':
            # Enterprise multi-tier
            if self._is_web_service(service_name, service_config):
                return ['sushi_web_tier', 'sushi_app_tier']
            elif self._is_data_service(service_name, service_config):
                return ['sushi_data_tier']
            elif self._is_mgmt_service(service_name, service_config):
                return ['sushi_mgmt_tier', 'sushi_app_tier']
            else:
                return ['sushi_app_tier']

        return ['default']

    def _is_web_service(self, service_name: str, service_config: Dict) -> bool:
        """Determine if service is a web-facing service"""
        web_services = ['caddy', 'homepage', 'grafana', 'n8n', 'code_server', 'jupyter']
        if service_name in web_services:
            return True

        # Check if service has exposed ports
        ports = service_config.get('ports', [])
        if ports and any('80' in str(port) or '443' in str(port) or '3000' in str(port) for port in ports):
            return True

        return False

    def _is_data_service(self, service_name: str, service_config: Dict) -> bool:
        """Determine if service is a data/storage service"""
        data_services = ['postgres', 'neo4j', 'redis', 'qdrant', 'weaviate', 'minio']
        return service_name in data_services

    def _is_mgmt_service(self, service_name: str, service_config: Dict) -> bool:
        """Determine if service is a management/monitoring service"""
        mgmt_services = ['prometheus', 'grafana', 'cadvisor', 'node_exporter']
        return service_name in mgmt_services

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Apply network security profiles to Docker Compose')
    parser.add_argument('--compose-file', required=True, help='Input Docker Compose file')
    parser.add_argument('--profile', required=True, choices=['chirashi', 'temaki', 'inari'],
                       help='Network security profile')
    parser.add_argument('--output', help='Output file (default: stdout)')

    args = parser.parse_args()

    # Load compose file
    try:
        with open(args.compose_file, 'r') as f:
            compose_dict = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Compose file '{args.compose_file}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        sys.exit(1)

    # Apply network configuration
    generator = NetworkConfigGenerator()
    try:
        result = generator.generate(compose_dict, args.profile)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Output result
    output_yaml = yaml.dump(result, default_flow_style=False, sort_keys=False)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_yaml)
        print(f"Network configuration applied and saved to {args.output}")
    else:
        print(output_yaml)

if __name__ == '__main__':
    main()