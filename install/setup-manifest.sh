#!/usr/bin/env bash
set -euo pipefail

echo "🍣 Sushi Kitchen — Manifest-Based Setup"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if generator exists
if [ ! -f "${REPO_ROOT}/scripts/generate-compose.py" ]; then
  echo "Error: Manifest generator not found. Run setup first."
  exit 1
fi

# Create .env if it doesn't exist
if [ ! -f "${REPO_ROOT}/.env" ]; then
  echo "-> Creating .env from .env.example"
  cp "${REPO_ROOT}/.env.example" "${REPO_ROOT}/.env"
else
  echo "-> .env already exists (will update keys if you choose)"
fi

# Create generated directory
mkdir -p "${REPO_ROOT}/compose/generated"

echo ""
echo "Available Platters:"
echo "=================="

# List available platters
python3 "${REPO_ROOT}/scripts/generate-compose.py" --list-platters 2>/dev/null || {
  echo "1. platter.starter (Starter Kitchen)"
  echo "2. platter.rag-workshop (RAG Workshop)"
  echo "3. platter.voice-agent (Voice Agent Starter)"
  echo "4. platter.creative-workbench (Creative Workbench)"
  echo "5. platter.observability-basic (Observability — Basic)"
  echo "6. platter.secure-team (Secure Team Workspace)"
  echo "7. platter.data-foundation (Data Foundation)"
  echo "8. platter.gpu-serving (GPU Serving Lab)"
  echo "9. platter.full-lab (Full AI Lab)"
}

echo ""
read -p "Select platter (1-9 or platter ID): " PLATTER_CHOICE

# Map choices to platter IDs
case "${PLATTER_CHOICE}" in
  1|platter.starter) PLATTER_ID="platter.starter" ;;
  2|platter.rag-workshop) PLATTER_ID="platter.rag-workshop" ;;
  3|platter.voice-agent) PLATTER_ID="platter.voice-agent" ;;
  4|platter.creative-workbench) PLATTER_ID="platter.creative-workbench" ;;
  5|platter.observability-basic) PLATTER_ID="platter.observability-basic" ;;
  6|platter.secure-team) PLATTER_ID="platter.secure-team" ;;
  7|platter.data-foundation) PLATTER_ID="platter.data-foundation" ;;
  8|platter.gpu-serving) PLATTER_ID="platter.gpu-serving" ;;
  9|platter.full-lab) PLATTER_ID="platter.full-lab" ;;
  *) PLATTER_ID="${PLATTER_CHOICE}" ;;
esac

# Update .env with selected platter
sed -i.bak -E "s/^(SELECTED_PLATTER=).*/\1${PLATTER_ID}/" "${REPO_ROOT}/.env"

echo ""
read -p "Include optional components? [y/N]: " INCLUDE_OPTIONAL
INCLUDE_OPTIONAL_FLAG=""
if [[ "${INCLUDE_OPTIONAL:-N}" =~ ^[Yy]$ ]]; then
  INCLUDE_OPTIONAL_FLAG="--include-optional"
fi

echo ""
echo "Generating Docker Compose for platter: ${PLATTER_ID}"

# Generate the compose file
python3 "${REPO_ROOT}/scripts/generate-compose.py" \
  --platter="${PLATTER_ID}" \
  ${INCLUDE_OPTIONAL_FLAG} \
  --output="${REPO_ROOT}/compose/generated/${PLATTER_ID}.yml"

echo ""
echo "✅ Generated compose file: compose/generated/${PLATTER_ID}.yml"
echo ""
echo "Next steps:"
echo "1. Review the generated compose file"
echo "2. Update .env with your specific configuration"
echo "3. Run: ./install/start-manifest.sh"
