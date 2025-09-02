#!/usr/bin/env bash
set -euo pipefail

echo "▶ Verifying Sushi Kitchen repo structure..."

required=(
  "compose/docker-compose.base.yml"
  "compose/docker-compose.obs.yml"
  "compose/docker-compose.devtools.yml"
  "compose/docker-compose.rag.yml"
  "compose/docker-compose.media.yml"
  "compose/docker-compose.cloud.yml"
  "compose/docker-compose.app.yml"
  "config/caddy/Caddyfile"
  "config/litellm/litellm.yaml"
  "config/prometheus/prometheus.yml"
  "config/grafana/provisioning/datasources/datasources.yaml"
  "docs/SETUP.md"
  "docs/menu.md"
  "docs/rolls/hosomaki.md"
  "scripts/sushi-start.sh"
  "scripts/sushi-stop.sh"
  "scripts/sushi-doctor.sh"
  ".cursorrules"
  "PRD.md"
  "ROADMAP.md"
  "CONTRIBUTING.md"
  "SUPPORT.md"
)

missing=0
for f in "${required[@]}"; do
  if [ ! -e "$f" ]; then
    echo "✗ Missing: $f"
    missing=$((missing+1))
  else
    echo "✓ $f"
  fi
done

# ----- Compose ignore check (smart, portable) -----
if [ -f .gitignore ]; then
  # Collect non-comment, non-negated lines that contain a broad compose ignore
  bad_compose_ignores="$(grep -nE 'docker-compose\.\*\.ya?ml' .gitignore 2>/dev/null \
    | grep -vE '^[[:space:]]*#' \
    | grep -vE '^[[:space:]]*!' || true)"

  if [ -n "${bad_compose_ignores}" ]; then
    echo
    echo "⚠️  Warning: .gitignore contains broad docker-compose ignore patterns without negation:"
    echo "${bad_compose_ignores}"
    echo "    → Keep only local overrides ignored (docker-compose.override.yml, docker-compose.local.yml)."
    echo "    → Ensure official files under compose/ stay tracked."
    # Warning only; do not fail.
  fi
fi

if [ "$missing" -gt 0 ]; then
  echo
  echo "❌ Repository missing $missing required item(s). Fix before pushing."
  exit 1
fi

echo
echo "✅ Structure OK."
