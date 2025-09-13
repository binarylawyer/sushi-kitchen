#!/usr/bin/env python3
"""
🍣 Sushi Kitchen — Template Assembler

This script assembles individual service templates into complete Docker Compose files.
It reads the manifest resolver output and combines the appropriate templates.
"""

import argparse
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Set

def load_template(template_path: Path) -> Dict:
    """Load a service template"""
    if not template_path.exists():
        return {}
    
    with open(template_path, 'r') as f:
        return yaml.safe_load(f)

def assemble_compose(roll_ids: Set[str], templates_dir: Path) -> Dict:
    """Assemble compose file from templates"""
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
        template_file = templates_dir / f"{roll_id}.yml"
        template = load_template(template_file)
        
        if template and 'services' in template:
            # Merge services
            for service_name, service_config in template['services'].items():
                compose['services'][service_name] = service_config
            
            # Merge volumes
            if 'volumes' in template:
                compose['volumes'].update(template['volumes'])
    
    return compose

def main():
    parser = argparse.ArgumentParser(description='Assemble Docker Compose from templates')
    parser.add_argument('--rolls', nargs='+', help='Roll IDs to include')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--templates-dir', default='compose/templates', help='Templates directory')
    
    args = parser.parse_args()
    
    if not args.rolls:
        parser.error('Must specify --rolls')
    
    templates_dir = Path(args.templates_dir)
    if not templates_dir.exists():
        print(f"Error: Templates directory '{templates_dir}' not found")
        sys.exit(1)
    
    roll_ids = set(args.rolls)
    compose = assemble_compose(roll_ids, templates_dir)
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            yaml.dump(compose, f, default_flow_style=False, sort_keys=False)
        print(f"Assembled compose file: {output_path}")
    else:
        print(yaml.dump(compose, default_flow_style=False, sort_keys=False))

if __name__ == '__main__':
    main()
