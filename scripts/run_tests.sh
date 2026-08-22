#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${TEST_PYTHON:-python3}"
cd "$ROOT_DIR"
TEST_PYTHON="$PYTHON" "$PYTHON" -m unittest discover -s tests -p 'test_*.py' -v
