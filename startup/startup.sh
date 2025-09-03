#!/bin/sh
# Sushi Kitchen start script – portable POSIX version

set -eu

# --- 0) Ensure interactive TTY if possible ---
if { [ ! -t 0 ] || [ ! -t 1 ]; } && [ -r /dev/tty ] && [ -w /dev/tty ]; then
  exec </dev/tty >/dev/tty 2>&1
fi

# --- 1) Find docker compose ---
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 ; then
  DC="docker compose"
elif command -v docker-compose >/dev/null 2>&1 ; then
  DC="docker-compose"
else
  echo "Error: Docker Compose not found. Install Docker Desktop (or docker-compose) and retry." >&2
  exit 1
fi

# --- 2) Base compose file (support both names) ---
if [ -f docker-compose.yml ]; then
  compose_args="-f docker-compose.yml"
elif [ -f docker.compose.yml ]; then
  compose_args="-f docker.compose.yml"
else
  echo "Error: no docker-compose.yml (or docker.compose.yml) found in repo root." >&2
  exit 1
fi

# --- 3) Require .env in repo root ---
if [ ! -f .env ]; then
  cat >&2 <<'EOF'

Error: .env not found in repo root.

Create one with at least:
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

# --- 4) Labels (menu text) ---
LABELS="Core (Hosomaki)
RAG (Futomaki)
Speech (Temaki)
Image (Uramaki)
Observability (Dragon)
Dev-tools (Tamago)
All-in (Omakase)"

print_menu() {
  i=1
  echo "Select one or more rolls (space-separated numbers)."
  echo "Press Enter for Core only."
  echo
  printf '%s\n' "$LABELS" | while IFS= read -r line ; do
    echo "  $i) $line"
    i=$(( i + 1 ))
  done
  echo
}

# --- 5) Selection: CLI numbers -> labels, else interactive (gum or numeric) ---
numbers_to_labels() {
  # $1: numbers string
  printf '%s\n' "$LABELS" \
    | nl -ba -w1 -s' ' \
    | awk -v sel="$1" '
        BEGIN { n=split(sel,a,/[^0-9]+/); for(i=1;i<=n;i++) pick[a[i]]=1; }
        pick[$1] { $1=""; sub(/^ +/,""); print }
      '
}

if [ "$#" -gt 0 ]; then
  # Allow: ./startup.sh 1 3 5
  nums="$*"
  SELECTED="$(numbers_to_labels "$nums")"
else
  if command -v gum >/dev/null 2>&1 && [ -t 0 ] && [ -t 1 ]; then
    echo "Use space to toggle, Enter to confirm:"
    SELECTED="$(printf '%s\n' "$LABELS" | gum choose --no-limit)"
    # If user hits Enter with nothing selected, SELECTED will be empty -> core only
  else
    print_menu
    printf "> "
    if read nums ; then : ; else nums=""; fi
    if [ -n "${nums:-}" ]; then
      SELECTED="$(numbers_to_labels "$nums")"
    else
      SELECTED=""
    fi
  fi
fi

# --- 6) Compute profiles (Core always on) ---
want_futomaki=false
want_temaki=false
want_uramaki=false
want_dragon=false
want_tamago=false

# Use here-doc so var changes persist in this shell
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

# --- 7) Include overlays if present ---
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
