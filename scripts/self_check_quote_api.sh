#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$ROOT_DIR/.env" ]; then
  set -a
  source "$ROOT_DIR/.env"
  set +a
fi

: "${QUOTE_API_BASE:?Missing QUOTE_API_BASE}"
: "${QUOTE_API_KEY:?Missing QUOTE_API_KEY}"

echo "HEALTH_OUTPUT"
curl -s "$QUOTE_API_BASE/health"
echo
echo "QUOTE_OUTPUT"
curl -s -X POST "$QUOTE_API_BASE/quote" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $QUOTE_API_KEY" \
  -d '{"school":"UCL","program":"Economics","degree_level":"UG","target_year":"2026/27","scope":"课程作业","total_words":32000}'
echo
