#!/usr/bin/env python3
"""Audit the package's three-skill boundary and public-release safety."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "dp-product-new-customer-quote",
    "dp-proposal-designer",
    "jizhi-academic-year-plan-proposal",
}
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".txt", ".example"}
SECRET_PATTERNS = (
    re.compile(r"QUOTE_API_KEY\s*=\s*['\"]?(?!replace-with-|your-)[A-Za-z0-9_-]{20,}"),
    re.compile(r"X-API-Key\s*:\s*(?!\$|\{)[A-Za-z0-9_-]{20,}"),
)
APPROVED_DUPLICATE_GROUPS = {
    frozenset({
        "skills/jizhi-academic-year-plan-proposal/scripts/export_pdf.py",
        "skills/dp-proposal-designer/scripts/export_pdf.py",
    }),
    # Each proposal skill must remain independently installable with its client-facing IP asset.
    frozenset({
        "skills/jizhi-academic-year-plan-proposal/assets/ip/study-dashboard.jpg",
        "skills/dp-proposal-designer/assets/ip/study-dashboard.jpg",
    }),
}


def fail(message: str) -> None:
    print("FAIL: " + message)
    global FAILED
    FAILED = True


FAILED = False
actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
if actual != EXPECTED:
    fail(f"skill directories must be exactly {sorted(EXPECTED)}; found {sorted(actual)}")

for name in EXPECTED:
    skill = SKILLS / name
    if not (skill / "SKILL.md").exists():
        fail(f"{name} is missing SKILL.md")
    if not (skill / "references" / "output_contracts.md").exists():
        fail(f"{name} is missing references/output_contracts.md")

required_runtime = (
    ROOT / "requirements-runtime.txt",
    ROOT / "scripts/bootstrap_runtime.sh",
    ROOT / "scripts/runtime_self_check.py",
    SKILLS / "jizhi-academic-year-plan-proposal/assets/schemas/intake.schema.json",
    SKILLS / "jizhi-academic-year-plan-proposal/assets/templates/template_contracts.json",
    SKILLS / "jizhi-academic-year-plan-proposal/assets/data/official_source_registry.json",
    SKILLS / "jizhi-academic-year-plan-proposal/scripts/build_planning_proposal.py",
    SKILLS / "jizhi-academic-year-plan-proposal/scripts/build_planning_quote.py",
    SKILLS / "jizhi-academic-year-plan-proposal/scripts/export_pdf.py",
    SKILLS / "jizhi-academic-year-plan-proposal/scripts/preflight_pdf.py",
    SKILLS / "jizhi-academic-year-plan-proposal/scripts/update_source_registry.py",
    SKILLS / "dp-proposal-designer/assets/schemas/intake.schema.json",
    SKILLS / "dp-proposal-designer/assets/templates/template_contracts.json",
    SKILLS / "dp-proposal-designer/scripts/build_dp_proposal.py",
    SKILLS / "dp-proposal-designer/scripts/export_pdf.py",
    SKILLS / "dp-product-new-customer-quote/assets/schemas/assessment_quote.schema.json",
    SKILLS / "dp-product-new-customer-quote/scripts/build_quote_workbook.py",
)
for path in required_runtime:
    if not path.exists():
        fail(f"missing runtime contract: {path.relative_to(ROOT)}")

quote_helper = SKILLS / "dp-product-new-customer-quote" / "scripts" / "quote_dp_api.py"
if not quote_helper.exists():
    fail("DP quote helper must live inside dp-product-new-customer-quote")

boundary_file = ROOT / "config" / "skill_boundaries.json"
if not boundary_file.exists():
    fail("missing config/skill_boundaries.json")
else:
    import json
    configured = set(json.loads(boundary_file.read_text(encoding="utf-8"))["skills"])
    if configured != EXPECTED:
        fail("boundary registry does not match installed skill directories")

hashes: dict[str, list[Path]] = {}
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    if ".git" in path.parts or "__pycache__" in path.parts or "tmp" in path.parts:
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    hashes.setdefault(digest, []).append(path)
    if path.suffix.lower() in TEXT_SUFFIXES or path.name == "SKILL.md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible credential in {path.relative_to(ROOT)}")

        if path.suffix.lower() == ".md":
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                if not (path.parent / target).resolve().exists():
                    fail(f"broken Markdown link in {path.relative_to(ROOT)}: {target}")

for paths in hashes.values():
    if len(paths) > 1:
        group = frozenset(str(p.relative_to(ROOT)) for p in paths)
        if group not in APPROVED_DUPLICATE_GROUPS:
            fail("duplicate files: " + ", ".join(sorted(group)))

for forbidden in (
    "dp-customer-visual-proposal",
    "jizhi-academic-planning-report",
    "jizhi-essay-customer-proposal",
    "assets/pricing",
    "极致服务组件价目表",
    "陪跑报价测试",
):
    if any(forbidden in str(path.relative_to(ROOT)) for path in ROOT.rglob("*")):
        fail(f"public package contains retired/private path: {forbidden}")

if FAILED:
    sys.exit(1)
print("PASS: three boundaries, runtime contracts, links, duplicates and public-secret checks")
