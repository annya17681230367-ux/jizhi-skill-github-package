#!/usr/bin/env python3
"""Choose one owning skill from a short request without loading skill content."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNDARIES = json.loads((ROOT / "config" / "skill_boundaries.json").read_text(encoding="utf-8"))

ANNUAL = (
    "学业规划", "全年规划", "陪跑", "专业课", "AI智慧学习系统", "规划报价", "课程规划",
    "个性化学业规划报告", "学业达成路径", "客户学业方案", "学业画像", "风险清单",
)
DP_PROPOSAL = ("DP方案", "DP安心包", "DP全包", "纯DP", "DP服务方案", "安心包方案", "全包作业方案")
DP_QUOTE = ("DP报价", "DP产品价格", "安心包报价", "Assessment报价", "assessment并报价", "作业量报价", "最终报价")


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def route(text: str) -> dict:
    annual = has_any(text, ANNUAL)
    proposal = has_any(text, DP_PROPOSAL)
    quote = has_any(text, DP_QUOTE)
    if "dp" in text.lower() and "报价" in text:
        quote = True
    if annual and "dp" in text.lower():
        proposal = True
        if "报价" in text:
            quote = True
    if annual and (proposal or quote):
        return {
            "owner": BOUNDARIES["mixed_owner"],
            "mode": "mixed",
            "components": [name for name, enabled in (
                ("dp-proposal-designer", proposal),
                ("dp-product-new-customer-quote", quote),
            ) if enabled],
        }
    if quote and proposal:
        return {"owner": "dp-proposal-designer", "mode": "dp_proposal_with_quote", "components": ["dp-product-new-customer-quote"]}
    if quote:
        return {"owner": "dp-product-new-customer-quote", "mode": "single", "components": []}
    if proposal:
        return {"owner": "dp-proposal-designer", "mode": "single", "components": []}
    return {"owner": "jizhi-academic-year-plan-proposal", "mode": "single", "components": []}


if __name__ == "__main__":
    request = " ".join(sys.argv[1:]).strip() or sys.stdin.read().strip()
    print(json.dumps(route(request), ensure_ascii=False, sort_keys=True))
