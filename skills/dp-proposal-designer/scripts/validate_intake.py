#!/usr/bin/env python3
"""Validate the canonical DP proposal intake."""

import json
import sys
from pathlib import Path

REQUIRED = ("contract", "version_status", "school", "program", "degree_level", "target_year", "scope", "target_score", "product", "situation", "risks", "courses")
CONTRACTS = {"D01", "D02", "D03"}
VERSIONS = {"v1 初稿", "v2 官网检索版", "v3 报价确认版", "v4 成交发送版"}


def validate(data: dict) -> list[str]:
    errors = [f"missing:{key}" for key in REQUIRED if data.get(key) in (None, "", [])]
    if data.get("contract") not in CONTRACTS:
        errors.append("invalid:contract")
    if data.get("version_status") not in VERSIONS:
        errors.append("invalid:version_status")
    if data.get("version_status") == "v4 成交发送版" and data.get("quote_status") not in {"已确认", "不含报价"}:
        errors.append("v4_requires_confirmed_quote_or_no_quote")
    return errors


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(data)
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, sort_keys=True))
    raise SystemExit(bool(errors))
