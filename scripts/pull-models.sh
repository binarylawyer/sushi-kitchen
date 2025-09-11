#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"
SHA_DIR="${ROOT_DIR}/models/shas"
OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"

function get_models_from_env() {
  local env_file="$1"
  if [ -f "${env_file}" ]; then
    grep -E '^OLLAMA_MODELS=' "${env_file}" | sed -E 's/^OLLAMA_MODELS=//' | tr -d '\"' | tr ',' ' '
  else
    echo ""
  fi
}

function model_present() {
  local name="$1"
  curl -s "${OLLAMA_HOST}/api/tags" | grep -q "\\\"name\\\":\\\"${name}\\\""
}

function pull_model() {
  local name="$1"
  echo "==> Pulling model: ${name}"
  curl -s -X POST "${OLLAMA_HOST}/api/pull" -d "{\"name\":\"${name}\"}" | jq -r '.status? // .message? // .error?' || true
}

function verify_checksum() {
  local name="$1"
  local safe_name
  safe_name="$(echo "${name}" | tr '/:' '__')"
  local sha_file="${SHA_DIR}/${safe_name}.sha256"
  if [ ! -f "${sha_file}" ]; then
    echo "    (no checksum file found for ${name}, skipping verify)"
    return 0
  fi
  local ollama_dir="${HOME}/.ollama/models"
  if [ ! -d "${ollama_dir}" ]; then
    echo "    (ollama models dir not found: ${ollama_dir}, skipping verify)"
    return 0
  fi
  echo "    verifying checksum(s) for ${name}"
  (cd "${ollama_dir}" && sha256sum -c "${sha_file}")
}

MODELS=("$@")
if [ "${#MODELS[@]}" -eq 0 ]; then
  read -r -a MODELS <<< "$(get_models_from_env "${ENV_FILE}")"
fi

if [ "${#MODELS[@]}" -eq 0 ]; then
  echo "No models specified (set OLLAMA_MODELS in .env or pass as args)."
  exit 1
fi

echo "Using OLLAMA_HOST=${OLLAMA_HOST}"
for m in "${MODELS[@]}"; do
  m="$(echo "${m}" | xargs)"
  [ -z "${m}" ] && continue
  if model_present "${m}"; then
    echo "==> Model already present: ${m}"
  else
    pull_model "${m}"
  fi
  verify_checksum "${m}" || { echo "!! checksum verification failed for ${m}"; exit 2; }
done

echo "All requested models are present."
