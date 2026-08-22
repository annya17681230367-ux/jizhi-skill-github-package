#!/usr/bin/env python3
"""Render contract-specific academic-planning HTML and warning sidecar."""

import argparse
import html
import json
from pathlib import Path

WARNING_PREFIX = "亲爱的学业规划师，您好！此次方案生成存在【预警提示】："


def e(value):
    return html.escape(str(value or ""))


def items(values):
    return "".join(f"<li>{e(value)}</li>" for value in values)


def section(title, body, cls=""):
    return f'<section class="{e(cls)}"><h2>{e(title)}</h2>{body}</section>'


def table(headers, rows):
    head = "".join(f"<th>{e(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{e(x)}</td>" for x in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def derive_warnings(data):
    warnings = list(data.get("warnings", [])) + list(data.get("pending", []))
    for course in data.get("courses", []):
        if course.get("workload_basis") in {"model_estimate", "pending"}:
            warnings.append(f"{course.get('code', '未知课程')}课程工作量不是已核实的官方数据")
        if not course.get("workload"):
            warnings.append(f"{course.get('code', '未知课程')}课程工作量待确认")
    seen = set()
    return [x for x in warnings if x and not (x in seen or seen.add(x))]


def course_service_match(data):
    rows = []
    for course in data.get("courses", []):
        workload = course.get("workload", "待确认")
        if course.get("workload_basis") == "model_estimate":
            workload = f"{workload}（模型预估，待人工审核）"
        rows.append((course.get("name"), course.get("code"), course.get("assessment"), workload, course.get("service")))
    return section("课程与服务匹配", table(("课程名称", "课程代码", "课程考核形式", "课程工作量", "匹配服务"), rows))


def context(data, label):
    tags = "".join(f'<span>{e(x)}</span>' for x in (data.get("degree_level"), data.get("target_period"), f"目标：{data.get('target') or ''}"))
    return f'<header><p>ACADEMIC PLANNING · {e(data.get("contract"))}</p><h1>{e(data.get("school"))}<br>{e(data.get("program"))} {e(label)}</h1><div class="tags">{tags}</div></header>'


def planning_grid(data, labels):
    cards = "".join(f"<article><b>{e(label)}</b><p>{e(data.get('planning_items', {}).get(label, '待补充'))}</p></article>" for label in labels)
    return section("学业规划模块", f'<div class="grid">{cards}</div>')


def timeline(data):
    rows = [(x.get("stage"), x.get("period", x.get("date")), x.get("action"), x.get("owner")) for x in data.get("timeline", [])]
    return section("阶段时间轴", table(("阶段", "时间", "行动", "负责人"), rows))


def execution(fixed):
    return section("每日 / 每周 / 每月执行", f"<ul>{items((fixed['daily'], fixed['weekly'], fixed['monthly']))}</ul>")


def ai_team(fixed, include_team=True):
    output = section(fixed["ai_title"], f'<p><b>{e(fixed["ai_positioning"])}</b></p><ul>{items(fixed["ai_functions"])}</ul>', "ai")
    if include_team:
        output += section("配套团队", f"<ul>{items(fixed['roles'])}</ul>")
    return output


def warning_section(warnings):
    if not warnings:
        return section("生成校验", "<p>本次未发现需要人工确认的特殊情况。</p>")
    return section("预警提示", f'<p class="warning-prefix">{e(WARNING_PREFIX)}</p><ul>{items(warnings)}</ul>', "warning")


def sources(data, fixed, warnings):
    links = "".join(f'<li><a href="{e(x.get("url"))}">{e(x.get("label"))}</a> · {e(x.get("source_year"))} · 核验于 {e(x.get("verified_at"))}</li>' for x in data.get("sources", []))
    return section("来源、边界与待确认", f"<ul>{links}</ul><p>{e(fixed['disclaimer'])}</p>") + warning_section(warnings)


def quote_block(data):
    quote = data.get("quote", {})
    rows = [(x.get("label"), x.get("quantity"), x.get("unit_price"), x.get("original"), x.get("discount"), x.get("final")) for x in quote.get("lines", [])]
    body = table(("项目", "数量", "单价", "原价", "折扣", "折后价"), rows)
    body += f'<div class="quote-total">原价：{e(quote.get("original_total", "待内部核价"))}　折后价：{e(quote.get("final_total", "待内部核价"))}</div>'
    body += f'<p>报价追溯ID：{e(quote.get("trace_id", "待生成"))}　审核状态：{e(quote.get("review_status", "待审核"))}</p>'
    return section("报价", body)


def render_contract(data, fixed, contracts, warnings):
    contract = data.get("contract", "T01")
    out = context(data, contracts[contract]["label"])
    if contract == "T00":
        out += section("学生情况", f"<ul>{items(data.get('student_profile', []))}</ul>")
        out += planning_grid(data, fixed["eight_items"]) + course_service_match(data) + sources(data, fixed, warnings)
    elif contract == "T01":
        out += section("学生基础", f"<ul>{items(data.get('student_profile', []))}</ul>")
        out += planning_grid(data, fixed["six_items"]) + course_service_match(data) + timeline(data) + execution(fixed) + ai_team(fixed)
        out += sources(data, fixed, warnings)
    elif contract == "T02":
        out += section("学生情况与服务定位", f"<ul>{items(data.get('student_profile', []))}</ul>")
        out += course_service_match(data) + timeline(data) + execution(fixed) + ai_team(fixed, include_team=False) + warning_section(warnings)
    elif contract == "T03":
        out += course_service_match(data) + quote_block(data) + warning_section(warnings)
    elif contract == "T05":
        out += course_service_match(data)
        out += section("产品责任边界", "<div class='split'><article><h3>DP范围</h3><p>经确认的写作、报告、展示或项目任务管理。</p></article><article><h3>学业规划与陪跑范围</h3><p>课程理解、专业课、考试训练、周执行和AI学习追踪。</p></article></div>")
        out += timeline(data) + quote_block(data) + warning_section(warnings)
    return out


def render(data, fixed, contracts, warnings):
    content = render_contract(data, fixed, contracts, warnings)
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data.get('school'))}学业规划</title><style>
@page{{size:A4;margin:12mm}}*{{box-sizing:border-box}}body{{margin:0;background:#eef6ff;color:#092d66;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.55}}main{{max-width:1080px;margin:auto;background:white}}header,section{{padding:28px 38px;border-bottom:1px solid #dce9f7}}h1{{font-size:32px}}h2{{font-size:21px}}.tags{{display:flex;gap:8px;flex-wrap:wrap}}.tags span{{background:#e6fffa;padding:5px 10px;border-radius:5px}}.grid,.split{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}article{{border:1px solid #cfe0f5;padding:14px;border-radius:8px}}table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{border:1px solid #cfe0f5;padding:8px;text-align:left;vertical-align:top}}th{{background:#eaf4ff}}.ai{{background:#edfffb;border-left:5px solid #08bda8}}.warning{{background:#fff8e8;border-left:5px solid #f59e0b}}.warning-prefix{{font-weight:700}}.quote-total{{font-size:20px;font-weight:700;color:#005cff;margin-top:16px}}@media(max-width:760px){{header,section{{padding:20px 16px}}.grid,.split{{grid-template-columns:1fr}}}}@media print{{body{{background:white}}section,article,table{{break-inside:avoid}}}}
</style></head><body><main>{content}</main></body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_html")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parent.parent
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    fixed = json.loads((skill / "assets/templates/planning_fixed_modules.json").read_text(encoding="utf-8"))
    contracts = json.loads((skill / "assets/templates/template_contracts.json").read_text(encoding="utf-8"))
    from validate_intake import validate
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid intake: " + ", ".join(errors))
    warnings = derive_warnings(data)
    output = Path(args.output_html)
    output.write_text(render(data, fixed, contracts, warnings), encoding="utf-8")
    output.with_suffix(output.suffix + ".warnings.json").write_text(json.dumps({"prefix": WARNING_PREFIX, "warnings": warnings}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output_html)


if __name__ == "__main__":
    main()
