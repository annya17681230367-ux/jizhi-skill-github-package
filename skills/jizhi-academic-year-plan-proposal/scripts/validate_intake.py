#!/usr/bin/env python3
"""Validate the stable annual-planning intake contract."""

import json
import sys
from pathlib import Path

REQUIRED = ("school", "program", "degree_level", "target_period", "student_profile", "target", "courses")
CONTRACTS = {"T01", "T02", "T03", "T05"}


def validate(data: dict) -> list[str]:
    errors = [f"missing:{key}" for key in REQUIRED if data.get(key) in (None, "", [])]
    if data.get("contract", "T01") not in CONTRACTS:
        errors.append("invalid:contract")
    for index, course in enumerate(data.get("courses", [])):
        for key in ("code", "name", "priority", "assessment", "service"):
            if course.get(key) in (None, ""):
                errors.append(f"courses[{index}].missing:{key}")
    return errors


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(data)
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, sort_keys=True))
    raise SystemExit(bool(errors))
