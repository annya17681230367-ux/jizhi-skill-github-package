#!/usr/bin/env python3
"""Store verified official university entry URLs without caching page facts."""

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--school", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--kind", required=True, choices=("programme", "module", "calendar", "assessment", "handbook"))
    parser.add_argument("--source-year", required=True)
    parser.add_argument("--verified-at", default=date.today().isoformat())
    args = parser.parse_args()
    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit("Only verified HTTPS official URLs may be cached.")
    path = Path(__file__).resolve().parent.parent / "assets/data/official_source_registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    school = data["schools"].setdefault(args.school, {"official_domains": [], "entries": []})
    if parsed.netloc not in school["official_domains"]:
        school["official_domains"].append(parsed.netloc)
    entry = {"url": args.url, "kind": args.kind, "source_year": args.source_year, "verified_at": args.verified_at}
    school["entries"] = [x for x in school["entries"] if not (x["url"] == args.url and x["kind"] == args.kind)]
    school["entries"].append(entry)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
