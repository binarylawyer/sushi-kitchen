#!/bin/sh
# Sushi Kitchen start script – POSIX‑compatible
# Works with /bin/sh or bash; no declare -A used.

set -eu

# 0) Check for Docker
if ! command -v docker >/dev/null 2>&1 ; then
  echo "Error: Docker is not installed or not in PATH." >&2
  exit 1
fi

# 1) Define menu labels (friendly names)
LABELS="Core (Hosomaki)
RAG (Futomaki)
Speech (Temaki)
Image (Uramaki)
Observability (Dragon)
Dev-tools (Tamago)
All-in (Omakase)"

# 2) Ask user to choose rolls, using gum if available
choose() {
  if command -v gum >/dev/null 2>&1 ; then
    printf '%s\n' "$LABELS" | gum choose --no-limit \
      --prompt="Which rolls? (space to select, Enter to confirm): "
    return
  fi

  # fallback prompt
  i=1
  echo "Pick rolls (space-separated numbers):"
  printf '%s\n' "$LABELS" | while IFS= read -r line ; do
    echo "  $i) $line"
    i=$(( i + 1 ))
  done
  printf "> "
  read -r nums || exit

  # Convert selected numbers to labels (newline-separated)
  printf '%s\n' "$LABELS" \
    | nl -ba -w1 -s' ' \
    | awk -v sel="$nums" '
        BEGIN { n=split(sel,a,/[^0-9]+/); for(i=1;i<=n;i++) pick[a[i]]=1; }
        pick[$1] { $1=""; sub(/^ +/,""); print }
      '
}

SELECTED="$(choose)"

# 3) Compute requested profiles – core (hosomaki) always enabled
want_futomaki=false
want_temaki=false
want_uramaki=false
want_dragon=false
want_tamago=false

printf '%s\n' "$SELECTED" | while IFS= read -r label ; do
  case "$label" in
    "RAG (Futomaki)")          want_futomaki=true   ;;
    "Speech (Temaki)")         want_temaki=true    ;;
    "Image (Uramaki)")         want_uramaki=true   ;;
    "Observability (Dragon)")  want_dragon=true    ;;
    "Dev-tools (Tamago)")      want_tamago=true    ;;
    "All-in (Omakase)")
      want_futomaki=true
      want_temaki=true
      want_uramaki=true
      want_dragon=true
      want_tamago=true
      ;;
    # Core (Hosomaki) is handled by default
  esac
done

# 4) Compose files – add overlays if they exist
compose_args="-f docker-compose.yml"
[ -f compose/docker-compose.obs.dragon.yml ] \
  && compose_args="$compose_args -f compose/docker-compose.obs.dragon.yml"
[ -f compose/docker-compose.media.uramaki.yml ] \
  && compose_args="$compose_args -f compose/docker-compose.media.uramaki.yml"
[ -f compose/docker-compose.rag.futomaki.yml ] \
  && compose_args="$compose_args -f compose/docker-compose.rag.futomaki.yml"
[ -f compose/docker-compose.devtools.tamago.yml ] \
  && compose_args="$compose_args -f compose/docker-compose.devtools.tamago.yml"

# 5) Build list of profiles to pass to docker compose
profile_args="--profile hosomaki"
[ "$want_futomaki" = true ] && profile_args="$profile_args --profile futomaki"
[ "$want_temaki"   = true ] && profile_args="$profile_args --profile temaki"
[ "$want_uramaki"  = true ] && profile_args="$profile_args --profile uramaki"
[ "$want_dragon"   = true ] && profile_args="$profile_args --profile dragon"
[ "$want_tamago"   = true ] && profile_args="$profile_args --profile tamago"

echo "Starting Sushi Kitchen with profiles:$profile_args"
# shellcheck disable=SC2086
exec sh -c "docker compose $compose_args $profile_args up -d"
