#!/usr/bin/env bash
set -Eeuo pipefail

# Friendly label -> compose profile
declare -A ROLL_TO_PROFILE
ROLL_TO_PROFILE["Core (Hosomaki)"]="hosomaki"
ROLL_TO_PROFILE["RAG (Futomaki)"]="futomaki"
ROLL_TO_PROFILE["Speech (Temaki)"]="temaki"
ROLL_TO_PROFILE["Image (Uramaki)"]="uramaki"
ROLL_TO_PROFILE["Observability (Dragon)"]="dragon"
ROLL_TO_PROFILE["Dev-tools (Tamago)"]="tamago"
ROLL_TO_PROFILE["All-in (Omakase)"]="omakase"

OPTIONS=(
  "Core (Hosomaki)"
  "RAG (Futomaki)"
  "Speech (Temaki)"
  "Image (Uramaki)"
  "Observability (Dragon)"
  "Dev-tools (Tamago)"
  "All-in (Omakase)"
)

choose_with_gum() {
  gum choose --no-limit "${OPTIONS[@]}"
}

choose_with_bash() {
  echo "Pick rolls (space-separated numbers):"
  for i in "${!OPTIONS[@]}"; do
    printf "  %d) %s\n" "$((i+1))" "${OPTIONS[$i]}"
  done
  read -r nums
  local out=""
  for n in $nums; do
    out+="${OPTIONS[$((n-1))]}"$'\n'
  done
  printf "%s" "$out"
}

if command -v gum >/dev/null 2>&1; then
  SELECTED="$(choose_with_gum || true)"
else
  SELECTED="$(choose_with_bash || true)"
fi

# Compute profiles (always include hosomaki)
declare -A WANT=()
WANT["hosomaki"]=1

while IFS= read -r label; do
  [[ -z "${label}" ]] && continue
  roll="${ROLL_TO_PROFILE[$label]}"
  if [[ "${roll}" == "omakase" ]]; then
    WANT["futomaki"]=1
    WANT["temaki"]=1
    WANT["uramaki"]=1
    WANT["dragon"]=1
    WANT["tamago"]=1
  else
    WANT["${roll}"]=1
  fi
done <<< "$SELECTED"

# Build args
profile_args=()
for p in "${!WANT[@]}"; do
  profile_args+=( "--profile" "${p}" )
done

# Compose files (add the overlays you actually use)
compose_args=( "-f" "docker-compose.yml" )
addf() { [[ -f "$1" ]] && compose_args+=( "-f" "$1" ); }
addf "compose/docker-compose.obs.dragon.yml"
addf "compose/docker-compose.media.uramaki.yml"
addf "compose/docker-compose.rag.futomaki.yml"
addf "compose/docker-compose.devtools.tamago.yml"

echo "Starting with profiles: ${profile_args[*]}"
docker compose "${compose_args[@]}" "${profile_args[@]}" up -d
