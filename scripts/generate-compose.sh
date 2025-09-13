#!/usr/bin/env bash
# Wrapper script for the Python generator

python3 "$(dirname "$0")/generate-compose.py" "$@"
