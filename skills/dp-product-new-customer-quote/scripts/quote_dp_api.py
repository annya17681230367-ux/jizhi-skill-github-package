#!/usr/bin/env python3
"""Call the private DP quote API without printing credentials."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REQUIRED_FIELDS = ("school", "program", "degree_level", "target_year", "scope", "total_words")


def load_dotenv() -> None:
    for parent in Path(__file__).resolve().parents:
        env_file = parent / ".env"
        if not env_file.exists():
            continue
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        return


def load_payload(args: argparse.Namespace) -> dict:
    if args.payload_json:
        return json.loads(args.payload_json)
    if args.payload_file:
        return json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def validate_payload(payload: dict) -> None:
    missing = [field for field in REQUIRED_FIELDS if payload.get(field) in (None, "")]
    if missing:
        raise SystemExit("Missing required payload fields: " + ", ".join(missing))
    try:
        total_words = int(payload["total_words"])
    except (TypeError, ValueError) as exc:
        raise SystemExit("total_words must be numeric") from exc
    if total_words <= 0:
        raise SystemExit("total_words must be greater than zero")


def request_quote(payload: dict) -> dict:
    load_dotenv()

    base = os.environ.get("QUOTE_API_BASE", "").rstrip("/")
    key = os.environ.get("QUOTE_API_KEY", "")
    if not base or not key:
        raise SystemExit("DP quote authorization is not configured on this machine.")

    validate_payload(payload)
    request = urllib.request.Request(
        f"{base}/quote",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-API-Key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"DP quote service returned HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"DP quote service is unavailable: {exc.reason}") from exc

    result = json.loads(body)
    if result.get("final_price") in (None, ""):
        raise SystemExit("DP quote service returned no final price.")
    return {
        field: result[field]
        for field in ("package_type", "scope", "original_price", "discount_rate", "final_price", "currency")
        if field in result
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Call the authorized private DP quote API.")
    parser.add_argument("payload_file", nargs="?", help="Optional JSON payload file")
    parser.add_argument("--payload-json", help="JSON payload string")
    args = parser.parse_args()
    public_result = request_quote(load_payload(args))
    print(json.dumps(public_result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
