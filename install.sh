#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"

mkdir -p "$SKILLS_DIR"

for skill in "$ROOT_DIR"/skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  target="$SKILLS_DIR/$name"
  if [ -e "$target" ]; then
    rm -rf "$target"
  fi
  cp -R "$skill" "$target"
  echo "Installed $name -> $target"
done

echo "Done. Restart Codex or start a new turn to use the skills."
