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

# Ensure we didn't accidentally ignore compose files or our meta dirs
if grep -R "docker-compose.*\.yml" .gitignore | grep -v override >/dev/null 2>&1; then
  echo "✗ Warning: .gitignore appears to ignore docker-compose files broadly. Please keep only 'docker-compose.override.yml' ignored."
  missing=$((missing+1))
fi

if [ "$missing" -gt 0 ]; then
  echo "\n❌ Repository missing $missing required items. Fix before pushing."
  exit 1
fi

echo "\n✅ Structure OK."
