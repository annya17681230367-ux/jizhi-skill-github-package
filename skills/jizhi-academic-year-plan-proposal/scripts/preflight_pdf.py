#!/usr/bin/env python3
"""Enforce the academic-planning PDF delivery gate and emit auditable results."""

import argparse
import json
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

CONTRACTS = {
    "T00": {"fixed_case": "固定模板00", "min_pages": 2, "max_pages": 2},
    "T01": {"fixed_case": "固定模板01", "min_pages": 3, "max_pages": 3},
    "T02": {"fixed_case": "固定模板02", "min_pages": 1, "max_pages": 1},
    "T03": {"fixed_case": "固定模板03", "min_pages": 1, "max_pages": 1},
    "T05": {"fixed_case": "固定模板05", "min_pages": 1, "max_pages": 1},
    "D01": {"fixed_case": "固定模板06", "min_pages": 3, "max_pages": 3},
}
FONT_STACK = '-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif'
INTERNAL_MARKERS = ("内部审核附件", "官方来源", "审核状态", "报价追溯", "亲爱的学业规划师", "模型估算")
GUARANTEE_PATTERNS = (r"保证通过", r"保证.{0,8}分", r"承诺.{0,8}成绩", r"百分之百通过", r"100%通过")
T01_MARKERS = (
    "ACADEMIC PLANNING", "学业画像与年度目标", "六大学业规划模块", "COURSE MATCH",
    "EXECUTION ROADMAP", "AI智慧学习系统", "每日", "每周", "每月", "配套团队",
)
REQUIRED_MARKERS = {
    "T00": ("ACADEMIC PLANNING", "个性化学业规划报告", "课程与服务匹配"),
    "T01": T01_MARKERS + ("五大支持体系", "学业规划", "AI智学系统", "押题支持", "陪跑执行", "专业课支持", "持续闭环"),
    "T02": ("课程考核与服务安排", "课程与服务匹配", "AI智慧学习系统"),
    "T03": ("课程与服务匹配", "服务报价", "原价", "折后价"),
    "T05": ("DP与学业规划服务分工", "课程与服务匹配"),
    "D01": ("DP ACADEMIC SUPPORT", "学生情况与核心风险", "课程与服务匹配", "DP安心包核心价值", "DP保障流程", "执行时间轴", "服务团队与质量控制", "启动所需资料"),
}
IP_REQUIRED = {"T00", "T01", "T05", "D01"}
NO_PRICE = {"T00", "T01", "T02", "D01"}


def runtime_python():
    config = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "jizhi-runtime/runtime.json"
    if config.exists():
        return json.loads(config.read_text(encoding="utf-8")).get("python")
    return None


def ensure_pypdf():
    try:
        import pypdf  # noqa: F401
    except ImportError:
        python = runtime_python()
        if python and Path(python).exists() and Path(python).absolute() != Path(sys.executable).absolute():
            os.execv(python, [python, __file__, *sys.argv[1:]])
        raise SystemExit("pypdf is missing. Run install.sh before PDF delivery.")


def infer_contract(html_text):
    match = re.search(r'<main class="contract-([TD]\d{2})"', html_text)
    return match.group(1) if match else ""


def pingfang_available():
    if platform.system() != "Darwin":
        return False
    known = Path("/System/Library/PrivateFrameworks/FontServices.framework/Resources/Reserved/PingFangUI.ttc")
    return known.exists()


def render_pngs(pdf, render_dir):
    renderer = shutil.which("pdftoppm")
    if not renderer:
        return [], "pdftoppm_missing"
    render_dir.mkdir(parents=True, exist_ok=True)
    for old in render_dir.glob("page-*.png"):
        old.unlink()
    prefix = render_dir / "page"
    subprocess.run([renderer, "-png", "-r", "130", str(pdf), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    images = sorted(render_dir.glob("page-*.png"))
    return images, ""


def valid_png(path):
    if path.stat().st_size < 5000:
        return False
    with path.open("rb") as stream:
        header = stream.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    width, height = struct.unpack(">II", header[16:24])
    return width >= 500 and height >= 700


def main():
    ensure_pypdf()
    from pypdf import PdfReader

    parser = argparse.ArgumentParser()
    parser.add_argument("input_html")
    parser.add_argument("output_pdf")
    parser.add_argument("--visual-reviewed", action="store_true")
    parser.add_argument("--font-fallback", default="")
    args = parser.parse_args()

    html_path = Path(args.input_html).resolve()
    pdf_path = Path(args.output_pdf).resolve()
    html_text = html_path.read_text(encoding="utf-8")
    contract = infer_contract(html_text)
    rule = CONTRACTS.get(contract)
    checks = {}
    checks["contract_confirmed"] = bool(rule)
    checks["fixed_generator_used"] = bool(rule) and f'data-fixed-template="{rule["fixed_case"]}"' in html_text
    checks["pdf_nonempty"] = pdf_path.exists() and pdf_path.stat().st_size >= 1000

    pages = len(PdfReader(str(pdf_path)).pages) if checks["pdf_nonempty"] else 0
    checks["page_count"] = bool(rule) and rule["min_pages"] <= pages <= rule["max_pages"]
    checks["font_stack"] = FONT_STACK in html_text
    native_font = pingfang_available()
    checks["font_available"] = native_font or bool(args.font_fallback)
    font_label = "PingFang SC" if native_font else (args.font_fallback or "UNAVAILABLE")

    checks["internal_content_absent"] = not any(marker in html_text for marker in INTERNAL_MARKERS)
    checks["removed_copy_absent"] = "方案价值" not in html_text
    checks["guaranteed_grade_claim_absent"] = not any(re.search(pattern, html_text) for pattern in GUARANTEE_PATTERNS)
    price_present = any(marker in html_text for marker in ("服务报价", "折后价", "原价"))
    checks["price_boundary"] = not price_present if contract in NO_PRICE else True

    internal_path = Path(str(html_path) + ".internal.json")
    internal = json.loads(internal_path.read_text(encoding="utf-8")) if internal_path.exists() else {}
    sources = internal.get("sources", [])
    checks["official_evidence"] = bool(sources) and all(str(item.get("url", "")).startswith(("http://", "https://")) for item in sources)
    checks["internal_sources_separated"] = internal_path.exists() and bool(sources)

    checks["required_sections"] = bool(rule) and all(marker in html_text for marker in REQUIRED_MARKERS[contract])
    checks["ip_policy"] = ('class="ip-hero"' in html_text and not any(x in html_text for x in ("mask:", "clip-path:", "filter:brightness", "opacity:0"))) if contract in IP_REQUIRED else 'class="ip-hero"' not in html_text
    checks["logo_policy"] = 'class="logo"' in html_text if contract in {"T00", "T01", "T03", "T05"} else 'class="logo"' not in html_text

    render_dir = pdf_path.with_suffix(".render")
    images, render_error = render_pngs(pdf_path, render_dir) if checks["pdf_nonempty"] else ([], "pdf_missing")
    checks["rendered_pngs"] = not render_error and len(images) == pages and all(valid_png(path) for path in images)
    checks["render_qa"] = checks["rendered_pngs"] and args.visual_reviewed

    static_checks = {key: value for key, value in checks.items() if key != "render_qa"}
    preflight_pass = all(static_checks.values()) and checks["render_qa"]
    price_declaration = "true" if contract in NO_PRICE else "not_applicable_for_quote_contract"
    declaration = (
        "已通过交付门禁：\n"
        f"contract={contract};\nfixed_case={rule['fixed_case'] if rule else 'UNCONFIRMED'};\n"
        f"pages={pages};\nfont={font_label};\nexport_chain=build_planning_proposal.py -> HeadlessChrome/Skia -> preflight_pdf.py;\n"
        f"render_qa={'已检查' if checks['render_qa'] else '未检查'};\nclient_pdf_no_price={price_declaration};\n"
        f"internal_sources_separated={'true' if checks['internal_sources_separated'] else 'false'};\n"
        f"no_guaranteed_grade_claim={'true' if checks['guaranteed_grade_claim_absent'] else 'false'}。"
    )
    result = {
        "preflight_pass": preflight_pass,
        "contract": contract,
        "fixed_case": rule["fixed_case"] if rule else "",
        "pages": pages,
        "font": font_label,
        "font_fallback": args.font_fallback or None,
        "export_chain": "build_planning_proposal.py -> HeadlessChrome/Skia -> preflight_pdf.py",
        "render_dir": str(render_dir),
        "rendered_pages": [str(path) for path in images],
        "checks": checks,
        "acceptance_declaration": declaration if preflight_pass else "未完成：交付门禁未全部通过。",
    }
    preflight_path = pdf_path.with_suffix(".preflight.json")
    preflight_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    pending_review = all(static_checks.values()) and checks["rendered_pngs"] and not args.visual_reviewed
    raise SystemExit(0 if preflight_pass else (2 if pending_review else 1))


if __name__ == "__main__":
    main()
