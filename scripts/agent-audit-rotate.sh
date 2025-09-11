#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${ROOT_DIR}/.logs"
LOG_FILE="${LOG_DIR}/agent-audit.jsonl"
MAX_ARCHIVES="${1:-7}"
MIN_SIZE="${2:-5242880}"

mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"

SIZE=$(wc -c < "${LOG_FILE}" || echo 0)
if [ "${SIZE}" -lt "${MIN_SIZE}" ]; then
  echo "agent-audit-rotate: size ${SIZE} < ${MIN_SIZE} (no rotation)."
  exit 0
fi

STAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
ARCHIVE="${LOG_DIR}/agent-audit-${STAMP}.jsonl.gz"

cp "${LOG_FILE}" "${LOG_FILE}.rotating"
: > "${LOG_FILE}"
gzip -c "${LOG_FILE}.rotating" > "${ARCHIVE}"
rm -f "${LOG_FILE}.rotating"

COUNT=$(ls -1 "${LOG_DIR}"/agent-audit-*.jsonl.gz 2>/dev/null | wc -l | tr -d ' ')
if [ "${COUNT}" -gt "${MAX_ARCHIVES}" ]; then
  ls -1t "${LOG_DIR}"/agent-audit-*.jsonl.gz | tail -n +$((MAX_ARCHIVES+1)) | xargs -r rm -f
fi

echo "agent-audit-rotate: done."
