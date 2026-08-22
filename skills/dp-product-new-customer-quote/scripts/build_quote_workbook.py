#!/usr/bin/env python3
"""Build a traceable five-sheet DP assessment and quote workbook."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

WARNING_PREFIX = "亲爱的学业规划师，您好！此次方案生成存在【预警提示】："
FIELDS = ("school", "program", "degree_level", "target_year", "scope", "assessments")
ASSESSMENT_FIELDS = ("course_code", "course_name", "term", "assessment", "weight", "official_workload", "equivalent_words", "workload_basis", "review_status", "source_url", "source_year", "evidence_status")


def ensure_runtime_python():
    if importlib.util.find_spec("openpyxl"):
        return
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    config_path = codex_home / "jizhi-runtime/runtime.json"
    if config_path.exists():
        python = json.loads(config_path.read_text(encoding="utf-8")).get("python")
        if python and Path(python).exists() and Path(python).absolute() != Path(sys.executable).absolute():
            os.execv(python, [python, __file__, *sys.argv[1:]])
    raise SystemExit("openpyxl is missing. Run the package install.sh to configure the Jizhi runtime.")


def validate(data: dict) -> list[str]:
    errors = [f"missing:{key}" for key in FIELDS if data.get(key) in (None, "", [])]
    for index, row in enumerate(data.get("assessments", [])):
        for key in ASSESSMENT_FIELDS:
            if row.get(key) in (None, ""):
                errors.append(f"assessments[{index}].missing:{key}")
        try:
            if int(row.get("equivalent_words", 0)) < 0:
                errors.append(f"assessments[{index}].invalid:equivalent_words")
        except (TypeError, ValueError):
            errors.append(f"assessments[{index}].invalid:equivalent_words")
        if row.get("workload_basis") == "model_estimate" and row.get("review_status") == "approved" and not data.get("reviewer"):
            errors.append(f"assessments[{index}].approved_estimate_requires:reviewer")
    return errors


def canonical_fingerprint(data: dict) -> str:
    keys = ("school", "program", "degree_level", "target_year", "scope", "package_type", "target_score", "assessments")
    payload = {key: data.get(key) for key in keys}
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def public_quote(quote: dict) -> dict:
    if quote.get("final_price") in (None, ""):
        raise ValueError("quote missing final_price")
    return {key: quote[key] for key in ("package_type", "scope", "original_price", "discount_rate", "final_price", "currency", "input_fingerprint", "quote_id", "quoted_at") if key in quote}


def warnings_for(data: dict, quote: dict, fingerprint: str, externally_bound: bool) -> list[str]:
    warnings = list(data.get("warnings", []))
    for row in data.get("assessments", []):
        code = row.get("course_code", "未知课程")
        if row.get("workload_basis") == "model_estimate":
            warnings.append(f"{code}报价工作量包含模型预估")
        if row.get("review_status") != "approved":
            warnings.append(f"{code}报价工作量尚未完成人工审核")
        if not row.get("source_url") or row.get("evidence_status") != "confirmed":
            warnings.append(f"{code}课程考核来源或证据状态待确认")
    if quote and quote.get("input_fingerprint") and quote["input_fingerprint"] != fingerprint:
        warnings.append("报价结果与当前课程工作量指纹不一致，价格已失效")
    if quote and not quote.get("input_fingerprint") and not externally_bound:
        warnings.append("外部报价未绑定当前输入，需人工审核后方可使用")
    if quote and ("original_price" not in quote or "discount_rate" not in quote):
        warnings.append("报价服务未返回完整原价或折扣字段")
    return list(dict.fromkeys(x for x in warnings if x))


def styles():
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    return {
        "navy": "0B2E63", "blue": "005CFF", "mint": "DFF8F3", "line": "C9D8EA", "warning": "FFF3CD",
        "Alignment": Alignment, "Border": Border, "Font": Font, "PatternFill": PatternFill, "Side": Side,
    }


def title(ws, text, span=14):
    s = styles()
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    cell = ws.cell(1, 1, text)
    cell.font = s["Font"](size=18, bold=True, color="FFFFFF")
    cell.fill = s["PatternFill"]("solid", fgColor=s["navy"])
    cell.alignment = s["Alignment"](horizontal="center")
    ws.sheet_view.showGridLines = False


def header(ws, row, values):
    s = styles()
    for col, value in enumerate(values, 1):
        cell = ws.cell(row, col, value)
        cell.font = s["Font"](bold=True, color="FFFFFF")
        cell.fill = s["PatternFill"]("solid", fgColor=s["blue"])
        cell.alignment = s["Alignment"](horizontal="center", vertical="center", wrap_text=True)


def build(data: dict, quote: dict, output: Path, trace: dict) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    except ImportError as exc:
        raise SystemExit("openpyxl is required: python3 -m pip install openpyxl") from exc

    wb = Workbook()
    summary = wb.active
    summary.title = "01课程考核汇总"
    title(summary, "课程 Assessment 汇总", 14)
    headers = ("序号", "课程代码", "课程名称", "学期", "Assessment", "占比", "官方工作量", "报价工作量", "工作量依据", "审核状态", "证据状态", "来源年份", "信息源", "备注")
    header(summary, 9, headers)
    for index, row in enumerate(data["assessments"], 10):
        values = (index - 9, row["course_code"], row["course_name"], row["term"], row["assessment"], row["weight"], row["official_workload"], int(row["equivalent_words"]), row["workload_basis"], row["review_status"], row["evidence_status"], row["source_year"], "来源", row.get("note", ""))
        for col, value in enumerate(values, 1):
            summary.cell(index, col, value).alignment = Alignment(vertical="top", wrap_text=True)
        summary.cell(index, 13).hyperlink = row["source_url"]
        summary.cell(index, 13).style = "Hyperlink"
    summary.freeze_panes = "A10"
    summary.auto_filter.ref = f"A9:N{9 + len(data['assessments'])}"

    service = wb.create_sheet("02课程与服务匹配")
    title(service, "课程与服务匹配", 5)
    header(service, 3, ("课程名称", "课程代码", "课程考核形式", "课程工作量", "匹配服务"))
    for index, row in enumerate(data["assessments"], 4):
        values = (row["course_name"], row["course_code"], row["assessment"], f'{row["official_workload"]} / 报价口径 {row["equivalent_words"]}', row.get("matched_service", "DP范围待确认"))
        for col, value in enumerate(values, 1):
            service.cell(index, col, value).alignment = Alignment(vertical="top", wrap_text=True)

    quote_ws = wb.create_sheet("03报价明细")
    title(quote_ws, "DP报价明细", 6)
    quote_rows = (
        ("套餐", quote.get("package_type", data.get("package_type", "待确认"))),
        ("覆盖范围", quote.get("scope", data["scope"])),
        ("报价工作量", trace["total_words"]),
        ("原价", quote.get("original_price", "待授权报价")),
        ("折扣", quote.get("discount_rate", "待授权报价")),
        ("折后价", quote.get("final_price", "待授权报价")),
        ("币种", quote.get("currency", "待确认")),
        ("输入指纹", trace["input_fingerprint"]),
        ("报价ID", quote.get("quote_id", "待确认")),
        ("报价时间", quote.get("quoted_at", trace["generated_at"])),
        ("人工审核", trace["review_status"]),
    )
    for row_index, (label, value) in enumerate(quote_rows, 3):
        quote_ws.cell(row_index, 1, label).font = Font(bold=True, color="0B2E63")
        quote_ws.merge_cells(start_row=row_index, start_column=2, end_row=row_index, end_column=6)
        quote_ws.cell(row_index, 2, value)

    source_ws = wb.create_sheet("04资料来源")
    title(source_ws, "资料来源", 6)
    header(source_ws, 3, ("课程代码", "课程名称", "来源年份", "证据状态", "核验日期", "官网链接"))
    for index, row in enumerate(data["assessments"], 4):
        values = (row["course_code"], row["course_name"], row["source_year"], row["evidence_status"], row.get("verified_at", "待记录"), "官网链接")
        for col, value in enumerate(values, 1):
            source_ws.cell(index, col, value).alignment = Alignment(vertical="top", wrap_text=True)
        source_ws.cell(index, 6).hyperlink = row["source_url"]
        source_ws.cell(index, 6).style = "Hyperlink"

    audit = wb.create_sheet("05内部审核")
    title(audit, "内部审核与预警", 4)
    audit_rows = (
        ("输入指纹", trace["input_fingerprint"]), ("生成时间", trace["generated_at"]),
        ("审核人", trace.get("reviewer") or "待填写"), ("审核状态", trace["review_status"]),
        ("工作量合计", trace["total_words"]), ("报价状态", trace["quote_status"]),
    )
    for row_index, (label, value) in enumerate(audit_rows, 3):
        audit.cell(row_index, 1, label).font = Font(bold=True)
        audit.cell(row_index, 2, value)
    warning_start = 11
    audit.cell(warning_start, 1, WARNING_PREFIX).font = Font(bold=True, color="9A6700")
    for offset, warning in enumerate(trace["warnings"], 1):
        audit.cell(warning_start + offset, 1, f"{offset}. {warning}")
        audit.merge_cells(start_row=warning_start + offset, start_column=1, end_row=warning_start + offset, end_column=4)
        audit.cell(warning_start + offset, 1).fill = PatternFill("solid", fgColor="FFF3CD")

    for ws in wb.worksheets:
        for col in range(1, ws.max_column + 1):
            ws.column_dimensions[chr(64 + col)].width = 18 if col < 13 else 22
        ws.sheet_view.showGridLines = False
    wb.save(output)


def main() -> int:
    ensure_runtime_python()
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_xlsx")
    parser.add_argument("--quote-json")
    parser.add_argument("--request-quote", action="store_true")
    parser.add_argument("--reviewer")
    args = parser.parse_args()
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    if args.reviewer:
        data["reviewer"] = args.reviewer
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid assessment input: " + ", ".join(errors))

    fingerprint = canonical_fingerprint(data)
    total_words = sum(int(x.get("equivalent_words", 0)) for x in data["assessments"])
    quote = {}
    externally_bound = False
    if args.quote_json:
        quote = public_quote(json.loads(Path(args.quote_json).read_text(encoding="utf-8")))
        externally_bound = bool(args.reviewer) or quote.get("input_fingerprint") == fingerprint
    elif args.request_quote:
        if total_words <= 0:
            raise SystemExit("Cannot request DP price with zero confirmed/estimated workload.")
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from quote_dp_api import request_quote
        payload = {key: data[key] for key in ("school", "program", "degree_level", "target_year", "scope")}
        payload["total_words"] = total_words
        for key in ("package_type", "target_score"):
            if data.get(key):
                payload[key] = data[key]
        quote = request_quote(payload)
        quote["input_fingerprint"] = fingerprint
        quote["quoted_at"] = datetime.now(timezone.utc).isoformat()
        externally_bound = True

    warnings = warnings_for(data, quote, fingerprint, externally_bound)
    all_approved = all(x.get("review_status") == "approved" for x in data["assessments"])
    quote_matches = not quote.get("input_fingerprint") or quote.get("input_fingerprint") == fingerprint
    review_status = "已审核" if all_approved and externally_bound and quote_matches else "待人工审核"
    trace = {
        "input_fingerprint": fingerprint,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_words": total_words,
        "reviewer": data.get("reviewer", ""),
        "review_status": review_status,
        "quote_status": "已绑定" if quote and externally_bound and quote_matches else "待绑定/待报价",
        "warnings": warnings,
    }
    output = Path(args.output_xlsx)
    build(data, quote, output, trace)
    output.with_suffix(output.suffix + ".trace.json").write_text(json.dumps({"trace": trace, "quote": quote}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output_xlsx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
