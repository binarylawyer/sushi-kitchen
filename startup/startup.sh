#!/bin/sh
# Sushi Kitchen start script – portable POSIX version
# Works with /bin/sh or bash; no associative arrays.

set -eu

# --- 0) Ensure interactive TTY for menus (reattach if piped/launched non-interactively) ---
if { [ ! -t 0 ] || [ ! -t 1 ]; } && [ -r /dev/tty ] && [ -w /dev/tty ]; then
  exec </dev/tty >/dev/tty 2>&1
fi

# --- 1) Tooling checks ---
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 ; then
  DC="docker compose"
elif command -v docker-compose >/dev/null 2>&1 ; then
  DC="docker-compose"
else
  echo "Error: Docker Compose not found. Install Docker Desktop (or docker-compose) and retry." >&2
  exit 1
fi

# --- 2) Base compose file detection (support both names) ---
if [ -f docker-compose.yml ]; then
  compose_args="-f docker-compose.yml"
elif [ -f docker.compose.yml ]; then
  compose_args="-f docker.compose.yml"
else
  echo "Error: no docker-compose.yml (or docker.compose.yml) found in repo root." >&2
  exit 1
fi

# --- 3) Require .env to avoid blank-substitution chaos ---
if [ ! -f .env ]; then
  cat >&2 <<'EOF'

Error: .env not found in repo root.

Create one (you can start from .env.example if present) with at least:
  POSTGRES_USER=sushi
  POSTGRES_PASSWORD=changeme
  POSTGRES_DB=sushi
  NEO4J_USER=neo4j
  NEO4J_PASSWORD=changeme
  N8N_ENCRYPTION_KEY=use-a-long-random-string

Then re-run:  ./startup/startup.sh

EOF
  exit 1
fi

# --- 4) Sushi roll labels (friendly names shown to the user) ---
LABELS="Core (Hosomaki)
RAG (Futomaki)
Speech (Temaki)
Image (Uramaki)
Observability (Dragon)
Dev-tools (Tamago)
All-in (Omakase)"

# --- 5) Ask the user to choose rolls ---
choose() {
  if command -v gum >/dev/null 2>&1 && [ -t 0 ] && [ -t 1 ]; then
    printf '%s\n' "$LABELS" \
      | gum choose --no-limit --prompt="Select rolls (space to toggle, Enter to confirm): "
    return
  fi

  i=1
  echo "Pick rolls (space-separated numbers). Press Enter for Core only:"
  printf '%s\n' "$LABELS" | while IFS= read -r line ; do
    echo "  $i) $line"
    i=$(( i + 1 ))
  done
  printf "> "
  if ! read -r nums ; then nums=""; fi
  [ -z "${nums:-}" ] && return 0

  # Convert selected numbers -> labels (newline-separated)
  printf '%s\n' "$LABELS" \
    | nl -ba -w1 -s' ' \
    | awk -v sel="$nums" '
        BEGIN { n=split(sel,a,/[^0-9]+/); for(i=1;i<=n;i++) pick[a[i]]=1; }
        pick[$1] { $1=""; sub(/^ +/,""); print }
      '
}

SELECTED="$(choose || true)"

# --- 6) Compute requested profiles (Core always on) ---
want_futomaki=false
want_temaki=false
want_uramaki=false
want_dragon=false
want_tamago=false

# Use a here-doc (not a pipeline) so variable changes persist in this shell
while IFS= read -r label ; do
  case "$label" in
    "RAG (Futomaki)")          want_futomaki=true ;;
    "Speech (Temaki)")         want_temaki=true ;;
    "Image (Uramaki)")         want_uramaki=true ;;
    "Observability (Dragon)")  want_dragon=true ;;
    "Dev-tools (Tamago)")      want_tamago=true ;;
    "All-in (Omakase)")
      want_futomaki=true
      want_temaki=true
      want_uramaki=true
      want_dragon=true
      want_tamago=true
      ;;
    *) : ;; # includes Core (Hosomaki)
  esac
done <<__END_SELECTED__
$SELECTED
__END_SELECTED__

# --- 7) Include overlay compose files if present ---
addf() { [ -f "$1" ] && compose_args="$compose_args -f $1"; }
addf "compose/docker-compose.obs.dragon.yml"
addf "compose/docker-compose.media.uramaki.yml"
addf "compose/docker-compose.rag.futomaki.yml"
addf "compose/docker-compose.devtools.tamago.yml"

# --- 8) Build profile flags ---
profile_args="--profile hosomaki"
[ "$want_futomaki" = true ] && profile_args="$profile_args --profile futomaki"
[ "$want_temaki"   = true ] && profile_args="$profile_args --profile temaki"
[ "$want_uramaki"  = true ] && profile_args="$profile_args --profile uramaki"
[ "$want_dragon"   = true ] && profile_args="$profile_args --profile dragon"
[ "$want_tamago"   = true ] && profile_args="$profile_args --profile tamago"

echo "Starting Sushi Kitchen with profiles:$profile_args"
# shellcheck disable=SC2086
exec sh -c "$DC $compose_args $profile_args up -d"
