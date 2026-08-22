#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
BACKUP_DIR="$CODEX_HOME/skill-backups/$(date +%Y%m%d-%H%M%S)"
EXPECTED=(dp-product-new-customer-quote dp-proposal-designer jizhi-academic-year-plan-proposal)
RETIRED=(dp-customer-visual-proposal)

mkdir -p "$SKILLS_DIR"
for name in "${RETIRED[@]}"; do
  target="$SKILLS_DIR/$name"
  if [ -e "$target" ]; then
    mkdir -p "$BACKUP_DIR"
    mv "$target" "$BACKUP_DIR/$name"
    echo "Quarantined retired competing skill $name -> $BACKUP_DIR/$name"
  fi
done
for name in "${EXPECTED[@]}"; do
  source_dir="$ROOT_DIR/skills/$name"
  target="$SKILLS_DIR/$name"
  if [ ! -f "$source_dir/SKILL.md" ]; then
    echo "Missing required skill: $name" >&2
    exit 1
  fi
  if [ -e "$target" ]; then
    mkdir -p "$BACKUP_DIR"
    mv "$target" "$BACKUP_DIR/$name"
    echo "Backed up $name -> $BACKUP_DIR/$name"
  fi
  cp -R "$source_dir" "$target"
  cmp "$source_dir/SKILL.md" "$target/SKILL.md"
  echo "Installed $name -> $target"
done
for name in jizhi-academic-planning-report jizhi-essay-customer-proposal; do
  if [ -e "$SKILLS_DIR/$name" ]; then
    echo "Notice: $name remains installed as a separate product; use explicit product wording when invoking skills."
  fi
done
echo "Installed exactly ${#EXPECTED[@]} skills. Restart Codex or start a new task."
