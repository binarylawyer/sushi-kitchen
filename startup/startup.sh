#!/bin/sh
# Sushi Kitchen start script – portable POSIX version
# Works with /bin/sh or bash. No associative arrays.

set -eu

# --- 0) Ensure we can interact (menu over /dev/tty if needed) ---
if { [ ! -t 0 ] || [ ! -t 1 ]; } && [ -r /dev/tty ] && [ -w /dev/tty ]; then
  exec </dev/tty >/dev/tty 2>&1
fi

# --- 1) Check prerequisites ---
if ! command -v docker >/dev/null 2>&1 ; then
  echo "Error: Docker is not installed or not in PATH." >&2
  exit 1
fi

# Require .env to avoid blank-substitution chaos
if [ ! -f .env ]; then
  cat >&2 <<'EOF'

Error: .env not found in the repo root.

Create one (you can start from .env.example if present) with at least:
  POSTGRES_USER=sushi
  POSTGRES_PASSWORD=changeme
  POSTGRES_DB=sushi
  NEO4J_USER=neo4j
  NEO4J_PASSWORD=changeme
  N8N_ENCRYPTION_KEY=use-a-long-random-string

Then re-run:  ./startup/start.sh

EOF
  exit 1
fi

# --- 2) Define menu labels (friendly names) ---
LABELS="Core (Hosomaki)
RAG (Futomaki)
Speech (Temaki)
Image (Uramaki)
Observability (Dragon)
Dev-tools (Tamago)
All-in (Omakase)"

# --- 3) Menu selection: gum if available, else numeric fallback ---
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
  # shellcheck disable=SC2162
  read nums || nums=""
  if [ -z "${nums:-}" ]; then
    # User chose nothing -> Core only
    return 0
  fi

  # Convert selected numbers to labels (newline-separated)
  printf '%s\n' "$LABELS" \
    | nl -ba -w1 -s' ' \
    | awk -v sel="$nums" '
        BEGIN { n=split(sel,a,/[^0-9]+/); for(i=1;i<=n;i++) pick[a[i]]=1; }
        pick[$1] { $1=""; sub(/^ +/,""); print }
      '
}

SELECTED="$(choose || true)"

# --- 4) Compute profiles – core is always on ---
want_futomaki=false
want_temaki=false
want_uramaki=false
want_dragon=false
want_tamago=false

printf '%s\n' "$SELECTED" | while IFS= read -r label ; do
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
done

# --- 5) Compose files – include overlays if they exist ---
compose_args="-f docker-compose.yml"
[ -f compose/docker-compose.obs.dragon.yml ]      && compose_args="$compose_args -f compose/docker-compose.obs.dragon.yml"
[ -f compose/docker-compose.media.uramaki.yml ]   && compose_args="$compose_args -f compose/docker-compose.media.uramaki.yml"
[ -f compose/docker-compose.rag.futomaki.yml ]    && compose_args="$compose_args -f compose/docker-compose.rag.futomaki.yml"
[ -f compose/docker-compose.devtools.tamago.yml ] && compose_args="$compose_args -f compose/docker-compose.devtools.tamago.yml"

# --- 6) Build profile flags ---
profile_args="--profile hosomaki"
[ "$want_futomaki" = true ] && profile_args="$profile_args --profile futomaki"
[ "$want_temaki"   = true ] && profile_args="$profile_args --profile temaki"
[ "$want_uramaki"  = true ] && profile_args="$profile_args --profile uramaki"
[ "$want_dragon"   = true ] && profile_args="$profile_args --profile dragon"
[ "$want_tamago"   = true ] && profile_args="$profile_args --profile tamago"

echo "Starting Sushi Kitchen with profiles:$profile_args"
# shellcheck disable=SC2086
exec sh -c "docker compose $compose_args $profile_args up -d"
