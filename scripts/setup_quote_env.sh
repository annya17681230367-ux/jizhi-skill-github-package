#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  cp "$ROOT_DIR/.env.example" "$ENV_FILE"
  echo "Created $ENV_FILE."
fi

set -a
source "$ENV_FILE"
set +a

if [ "${QUOTE_API_BASE:-}" = "replace-with-private-quote-api-url" ] || [ -z "${QUOTE_API_BASE:-}" ]; then
  read -r -p "QUOTE_API_BASE: " QUOTE_API_BASE
fi

if [ "${QUOTE_API_KEY:-}" = "replace-with-private-quote-api-key" ] || [ -z "${QUOTE_API_KEY:-}" ]; then
  read -r -s -p "QUOTE_API_KEY: " QUOTE_API_KEY
  echo
fi

if [ -z "${QUOTE_API_BASE:-}" ] || [ -z "${QUOTE_API_KEY:-}" ]; then
  echo "Missing QUOTE_API_BASE or QUOTE_API_KEY." >&2
  exit 1
fi

cat > "$ENV_FILE" <<EOF
QUOTE_API_BASE="$QUOTE_API_BASE"
QUOTE_API_KEY="$QUOTE_API_KEY"
EOF

for rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
  touch "$rc"
  if grep -q '^export QUOTE_API_BASE=' "$rc"; then
    sed -i.bak 's|^export QUOTE_API_BASE=.*$|export QUOTE_API_BASE="'"$QUOTE_API_BASE"'"|' "$rc"
  else
    echo "export QUOTE_API_BASE=\"$QUOTE_API_BASE\"" >> "$rc"
  fi
  if grep -q '^export QUOTE_API_KEY=' "$rc"; then
    sed -i.bak 's|^export QUOTE_API_KEY=.*$|export QUOTE_API_KEY="'"$QUOTE_API_KEY"'"|' "$rc"
  else
    echo "export QUOTE_API_KEY=\"$QUOTE_API_KEY\"" >> "$rc"
  fi
done

echo "Quote environment variables written to ~/.zshrc and ~/.bashrc."
echo "Secrets are stored only in local shell files and .env; do not commit them."
