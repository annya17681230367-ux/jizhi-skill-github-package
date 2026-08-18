#!/usr/bin/env python3
"""Call the private DP quote API without exposing secrets in logs.

Usage:
  python3 scripts/quote_dp_api.py --payload-json '{"school":"UCL",...}'
  python3 scripts/quote_dp_api.py payload.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


REQUIRED_FIELDS = ["school", "program", "degree_level", "target_year", "scope", "total_words"]


def load_dotenv(repo_root: Path) -> None:
    env_file = repo_root / ".env"
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def load_payload(args: argparse.Namespace) -> dict:
    if args.payload_json:
        return json.loads(args.payload_json)
    if args.payload_file:
        return json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def validate_payload(payload: dict) -> None:
    missing = [field for field in REQUIRED_FIELDS if payload.get(field) in (None, "")]
    if missing:
        raise SystemExit(f"Missing required payload fields: {', '.join(missing)}")
    try:
        int(payload["total_words"])
    except (TypeError, ValueError):
        raise SystemExit("total_words must be numeric")


def main() -> int:
    parser = argparse.ArgumentParser(description="Call private DP quote API.")
    parser.add_argument("payload_file", nargs="?", help="Optional JSON payload file.")
    parser.add_argument("--payload-json", help="JSON payload string.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(repo_root)

    base = os.environ.get("QUOTE_API_BASE", "").rstrip("/")
    key = os.environ.get("QUOTE_API_KEY", "")
    if not base or not key:
        raise SystemExit("Missing QUOTE_API_BASE or QUOTE_API_KEY. Run scripts/setup_quote_env.sh on an authorized machine.")
    if base.startswith("replace-with-") or key.startswith("replace-with-"):
        raise SystemExit("QUOTE_API_BASE or QUOTE_API_KEY is still a placeholder.")

    payload = load_payload(args)
    validate_payload(payload)

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/quote",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        safe_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Quote API HTTP {exc.code}: {safe_body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Quote API connection failed: {exc.reason}") from exc

    result = json.loads(body)
    if not result.get("final_price"):
        raise SystemExit(f"Quote API returned no final_price: {body}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
