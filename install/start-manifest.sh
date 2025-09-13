#!/usr/bin/env bash
set -euo pipefail

echo "🍣 Sushi Kitchen — Start from Manifest"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Please install Docker & the Compose plugin."; exit 1
fi

if [ ! -f ".env" ]; then
  echo ".env not found. Run ./install/setup-manifest.sh first."; exit 1
fi

# Get selected platter from .env
SELECTED_PLATTER="$(grep -E '^SELECTED_PLATTER=' .env | sed -E 's/^SELECTED_PLATTER=//' || echo '')"

if [ -z "${SELECTED_PLATTER}" ]; then
  echo "No platter selected. Run ./install/setup-manifest.sh first."; exit 1
fi

COMPOSE_FILE="compose/generated/${SELECTED_PLATTER}.yml"

if [ ! -f "${COMPOSE_FILE}" ]; then
  echo "Compose file not found: ${COMPOSE_FILE}"
  echo "Run ./install/setup-manifest.sh to generate it."; exit 1
fi

echo "Validating docker compose configuration..."
docker compose -f "${COMPOSE_FILE}" config >/dev/null

echo "Starting platter: ${SELECTED_PLATTER}"
echo "Using compose file: ${COMPOSE_FILE}"

docker compose -f "${COMPOSE_FILE}" up -d

echo "Done. Services starting in background."
echo ""
echo "To view logs: docker compose -f ${COMPOSE_FILE} logs -f"
echo "To stop: docker compose -f ${COMPOSE_FILE} down"
