#!/usr/bin/env bash
set -euo pipefail

echo "🍣 Sushi Kitchen — Interactive Setup"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -f "${REPO_ROOT}/.env" ]; then
  echo "-> Creating .env from .env.example"
  cp "${REPO_ROOT}/.env.example" "${REPO_ROOT}/.env"
else
  echo "-> .env already exists (will update keys if you choose)"
fi

read -p "Select profile [core/full] (default: core): " PROFILE
PROFILE="${PROFILE:-core}"
if [[ "${PROFILE}" != "core" && "${PROFILE}" != "full" ]]; then
  echo "Invalid profile. Use 'core' or 'full'."; exit 1
fi
sed -i.bak -E "s/^(STACK_PROFILE=).*/\1${PROFILE}/" "${REPO_ROOT}/.env"

read -p "Enable observability (Grafana/Prom/Langfuse)? [y/N]: " OBS
if [[ "${OBS:-N}" =~ ^[Yy]$ ]]; then
  sed -i -E "s/^(ENABLE_OBSERVABILITY=).*/\1true/" "${REPO_ROOT}/.env"
else
  sed -i -E "s/^(ENABLE_OBSERVABILITY=).*/\1false/" "${REPO_ROOT}/.env"
fi

read -p "Enable media services (ComfyUI)? [y/N]: " MED
if [[ "${MED:-N}" =~ ^[Yy]$ ]]; then
  sed -i -E "s/^(ENABLE_MEDIA=).*/\1true/" "${REPO_ROOT}/.env"
else
  sed -i -E "s/^(ENABLE_MEDIA=).*/\1false/" "${REPO_ROOT}/.env"
fi

read -p "Enable extras (Portainer, Flowise, etc.)? [y/N]: " EX
if [[ "${EX:-N}" =~ ^[Yy]$ ]]; then
  sed -i -E "s/^(ENABLE_EXTRAS=).*/\1true/" "${REPO_ROOT}/.env"
else
  sed -i -E "s/^(ENABLE_EXTRAS=).*/\1false/" "${REPO_ROOT}/.env"
fi

read -p "Supabase URL (or leave blank to skip): " SUPA_URL
if [ -n "${SUPA_URL}" ]; then
  sed -i -E "s|^(NEXT_PUBLIC_SUPABASE_URL=).*|\1${SUPA_URL}|" "${REPO_ROOT}/.env"
fi
read -p "Supabase anon public key (or leave blank to skip): " SUPA_KEY
if [ -n "${SUPA_KEY}" ]; then
  sed -i -E "s|^(NEXT_PUBLIC_SUPABASE_ANON_KEY=).*|\1${SUPA_KEY}|" "${REPO_ROOT}/.env"
fi

read -p "Enable LiteLLM cloud gateway? [y/N]: " LLMG
if [[ "${LLMG:-N}" =~ ^[Yy]$ ]]; then
  sed -i -E "s/^(LITELLM_ENABLE=).*/\1true/" "${REPO_ROOT}/.env"
  read -p "OpenAI API key (optional): " OPENAI
  [ -n "${OPENAI}" ] && sed -i -E "s|^(OPENAI_API_KEY=).*|\1${OPENAI}|" "${REPO_ROOT}/.env"
  read -p "Anthropic API key (optional): " ANTH
  [ -n "${ANTH}" ] && sed -i -E "s|^(ANTHROPIC_API_KEY=).*|\1${ANTH}|" "${REPO_ROOT}/.env"
else
  sed -i -E "s/^(LITELLM_ENABLE=).*/\1false/" "${REPO_ROOT}/.env"
fi

echo "If you have an NVIDIA GPU, ensure nvidia-container-toolkit is installed."
echo "Setup complete. You can now run ./install/start.sh"
