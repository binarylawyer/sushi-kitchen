#!/usr/bin/env bash
set -euo pipefail

echo "🍣 Sushi Kitchen — Start Script"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Please install Docker & the Compose plugin."; exit 1
fi

if [ ! -f ".env" ]; then
  echo ".env not found. Run ./install/setup.sh first."; exit 1
fi

echo "Validating docker compose configuration..."
docker compose config >/dev/null

PROFILE="$(grep -E '^STACK_PROFILE=' .env | sed -E 's/^STACK_PROFILE=//')"
PROFILE="${PROFILE:-core}"

if [[ "${PROFILE}" == "core" ]]; then
  echo "Starting CORE profile..."
  docker compose --profile core up -d
else
  echo "Starting FULL profile..."
  docker compose up -d
fi

echo "Done. Services starting in background."
grep -E '^(PORT_|ENABLE_|STACK_PROFILE|OLLAMA_)' .env | sed -E 's/^/  /'
