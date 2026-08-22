#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
RUNTIME_DIR="$CODEX_HOME/jizhi-runtime"
VENV_DIR="$RUNTIME_DIR/venv"
CONFIG_FILE="$RUNTIME_DIR/runtime.json"
BASE_PYTHON="${JIZHI_BASE_PYTHON:-python3}"

mkdir -p "$RUNTIME_DIR"
if [ ! -x "$VENV_DIR/bin/python" ]; then
  "$BASE_PYTHON" -m venv "$VENV_DIR"
fi
RUNTIME_PYTHON="$VENV_DIR/bin/python"
"$RUNTIME_PYTHON" -m pip install --disable-pip-version-check --quiet -r "$ROOT_DIR/requirements-runtime.txt"

find_browser() {
  for candidate in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "$(command -v google-chrome 2>/dev/null || true)" \
    "$(command -v chromium 2>/dev/null || true)" \
    "$(command -v chromium-browser 2>/dev/null || true)"; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then
      printf '%s' "$candidate"
      return 0
    fi
  done
  return 1
}

BROWSER="${JIZHI_CHROMIUM_PATH:-}"
if [ -z "$BROWSER" ]; then
  BROWSER="$(find_browser || true)"
fi
if [ -z "$BROWSER" ]; then
  echo "No local Chrome/Edge found; installing isolated Playwright Chromium..."
  "$RUNTIME_PYTHON" -m pip install --disable-pip-version-check --quiet 'playwright>=1.50,<2'
  "$RUNTIME_PYTHON" -m playwright install chromium
  BROWSER="$($RUNTIME_PYTHON - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print(p.chromium.executable_path)
PY
)"
fi
if [ ! -x "$BROWSER" ]; then
  echo "Unable to configure a Chromium executable for PDF output." >&2
  exit 1
fi

"$RUNTIME_PYTHON" - "$CONFIG_FILE" "$RUNTIME_PYTHON" "$BROWSER" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
path, python, browser = map(Path, sys.argv[1:])
payload = {
    "version": 1,
    "python": str(python.absolute()),
    "browser": str(browser.resolve()),
    "checked_at": datetime.now(timezone.utc).isoformat(),
}
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
PY
"$RUNTIME_PYTHON" "$ROOT_DIR/scripts/runtime_self_check.py" --browser "$BROWSER"
echo "Jizhi runtime configured -> $CONFIG_FILE"
