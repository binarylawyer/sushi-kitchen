#!/usr/bin/env bash
# Sushi Kitchen start script (interactive)
#
# This script allows you to start the Sushi Kitchen stack by selecting
# which "rolls" (Docker Compose profiles) you want to enable.  Each roll
# corresponds to a set of optional services (packs) described in the
# documentation.  The core roll (hosomaki) is always required and
# automatically included.

set -euo pipefail

# Define the mapping between friendly names and compose profile names.
declare -A ROLL_TO_PROFILE=(
  ["Core (Hosomaki)"]=hosomaki
  ["RAG (Futomaki)"]=futomaki
  ["Speech (Temaki)"]=temaki
  ["Image (Uramaki)"]=uramaki
  ["Agents (Agentic)"]=agent
  ["Observability (Dragon)"]=dragon
  ["MLops (Spider)"]=spider
  ["Inference‑pro (Gunkanmaki)"]=gunkanmaki
  ["Dev‑tools (Tamago)"]=tamago
  ["All‑in (Omakase)"]=omakase
)

# Build an array of menu options from the keys of the associative array
OPTIONS=("${!ROLL_TO_PROFILE[@]}")

echo "\n🎌 Welcome to Sushi Kitchen!"
echo "Select the rolls you want to enable:"

# If gum is installed, use it for multi‑select UI; otherwise fall back to Bash select
if command -v gum >/dev/null 2>&1; then
  # Use gum choose with multi‑select
  SELECTED=$(printf "%s\n" "${OPTIONS[@]}" | gum choose --no-limit --prompt="Which rolls? (space to select, enter to confirm): ")
else
  # Bash fallback: ask for space‑separated numbers
  i=1
  for opt in "${OPTIONS[@]}"; do
    printf "%2d) %s\n" "$i" "$opt"
    i=$((i+1))
  done
  echo -n "Enter numbers separated by spaces (e.g. 1 3 4): "
  read -r nums
  for n in $nums; do
    # shellcheck disable=SC2219
    SELECTED+="${OPTIONS[$((n-1))]}\n"
  done
fi

# Always include the core profile
PROFILES=(hosomaki)

while read -r choice; do
  # Skip empty lines
  [[ -z "$choice" ]] && continue
  profile=${ROLL_TO_PROFILE[$choice]}
  # Omakase = all profiles
  if [[ $profile == omakase ]]; then
    PROFILES=(hosomaki futomaki temaki uramaki agent dragon spider gunkanmaki tamago)
    break
  fi
  # Avoid adding duplicate profiles
  [[ " ${PROFILES[*]} " == *" $profile "* ]] || PROFILES+=("$profile")
done <<<"$SELECTED"

# Print summary
echo "\nYou have selected: ${PROFILES[*]}"

# Build the docker compose command
CMD=("docker" "compose")
for p in "${PROFILES[@]}"; do
  CMD+=("--profile" "$p")
done
CMD+=("up" "-d")

echo "Running: ${CMD[*]}"
"${CMD[@]}"