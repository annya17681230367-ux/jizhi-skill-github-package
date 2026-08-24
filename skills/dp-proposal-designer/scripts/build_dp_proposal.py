#!/usr/bin/env python3
"""Render a client DP proposal and a separate internal audit artifact."""

import argparse
import html
import json
from pathlib import Path

WARNING_PREFIX = "亲爱的学业规划师，您好！此次方案生成存在【预警提示】："


def e(value):
    return html.escape(str(value or ""))


def items(values):
    return "".join(f"<li>{e(x)}</li>" for x in values if x)


def table(headers, rows):
    return "<table><thead><tr>" + "".join(f"<th>{e(x)}</th>" for x in headers) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(x)}</td>" for x in row) + "</tr>" for row in rows) + "</tbody></table>"


def warnings_for(data):
    warnings = list(data.get("warnings", []))
    for course in data.get("courses", []):
        if course.get("workload_basis") in {"model_estimate", "pending"} or not course.get("workload"):
            warnings.append(f"{course.get('code', '未知课程')}课程工作量需人工确认")
    return list(dict.fromkeys(x for x in warnings if x))


def course_rows(data, internal=False):
    output = []
    for course in data.get("courses", []):
        workload = course.get("workload") or "待课程文件确认"
        if internal and course.get("workload_basis") == "model_estimate":
            workload += "（模型估算）"
        output.append((course.get("code"), course.get("name"), course.get("assessment"), workload, course.get("service_focus")))
    return output


def fixed_cards(title, values):
    cards = "".join(f'<article><b>{i + 1:02d}</b><p>{e(value)}</p></article>' for i, value in enumerate(values))
    return f'<section><div class="section-title"><span>FIXED VALUE</span><h2>{e(title)}</h2></div><div class="grid">{cards}</div></section>'


def client_html(data, fixed):
    contract = data.get("contract", "D01")
    situation_text = "".join(f"<p>{e(x)}</p>" for x in data.get("situation", []))
    risk_cards = "".join(
        f'<article><h3>{e(x.get("title"))}</h3><p>{e(x.get("detail"))}</p></article>'
        for x in data.get("risks", [])
    )
    situation = "" if contract == "D02" else f'<section class="overview"><div><div class="section-title"><span>STUDENT CONTEXT</span><h2>学生情况与核心风险</h2></div>{situation_text}</div><div class="risk-grid">{risk_cards}</div></section>'
    course_map = table(("课程代码", "课程名称", "考核形式", "工作量", "匹配服务"), course_rows(data))
    timeline = table(("阶段", "时间", "执行动作", "学生需提供"), [(x.get("stage"), x.get("date"), x.get("action"), x.get("student_input")) for x in data.get("timeline", [])])
    materials = items(data.get("materials_required", []))
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data.get("school"))} DP服务方案</title><style>
@page{{size:A4;margin:0}}*{{box-sizing:border-box}}:root{{--ink:#10204b;--blue:#075ff2;--cyan:#08c8bb;--purple:#7566f2;--line:#d7e5f5}}body{{margin:0;background:#eaf2ff;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.55}}main{{width:210mm;min-height:297mm;margin:auto;background:white}}header,section{{padding:10mm 15mm;border-bottom:1px solid #e6eef8}}header{{padding-top:18mm;color:white;background:linear-gradient(135deg,#082c79 0%,#0768eb 48%,#08bcae 100%)}}.eyebrow,.section-title span{{font-size:10px;font-weight:800;letter-spacing:1.3px;color:#09a999}}header .eyebrow{{color:#84fff2}}h1{{font-size:31px;line-height:1.2;margin:6px 0 12px}}.tags{{display:flex;gap:7px;flex-wrap:wrap}}.tags span{{font-size:11px;padding:4px 9px;border:1px solid rgba(255,255,255,.45);border-radius:5px;background:rgba(255,255,255,.12)}}.section-title{{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}}h2{{font-size:20px;margin:0}}h3{{font-size:13px;margin:0 0 4px}}p,li{{font-size:12px}}.overview{{display:grid;grid-template-columns:1fr 1.25fr;gap:20px}}.risk-grid,.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}}article{{padding:11px;border:1px solid var(--line);border-radius:6px;background:#fbfdff}}article b{{font-size:18px;color:var(--cyan)}}article p{{margin:3px 0;color:#5b6b82}}table{{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--line);border-radius:6px;overflow:hidden;font-size:10px}}th,td{{padding:7px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);vertical-align:top;text-align:left}}th:last-child,td:last-child{{border-right:0}}tr:last-child td{{border-bottom:0}}th{{background:#eaf4ff}}.assurance{{color:white;background:#10295f}}.assurance h2,.assurance .section-title span{{color:white}}.assurance .grid article{{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.18)}}.assurance article p{{color:white}}.materials{{background:#edfffb}}@media(max-width:760px){{main{{width:100%}}.overview,.risk-grid,.grid{{grid-template-columns:1fr}}}}@media print{{body{{background:white}}header,section,article,table{{break-inside:avoid}}}}
</style></head><body><main><header><div class="eyebrow">DP ACADEMIC SUPPORT</div><h1>{e(data.get("school"))}<br>{e(data.get("program"))} DP服务方案</h1><div class="tags"><span>{e(data.get("target_year"))}</span><span>目标：{e(data.get("target_score"))}</span><span>{e(data.get("product"))}</span><span>{e(data.get("scope"))}</span></div></header>
{situation}<section><div class="section-title"><span>COURSE MATCH</span><h2>课程与服务匹配</h2></div>{course_map}</section>
{fixed_cards(fixed["core_value_title"], fixed["core_value"])}
<section class="assurance page-two"><div class="section-title"><span>EXECUTION SYSTEM</span><h2>{e(fixed["assurance_process_title"])}</h2></div><div class="grid">{"".join(f"<article><p>{e(x)}</p></article>" for x in fixed["assurance_process"])}</div></section>
<section><div class="section-title"><span>TIMELINE</span><h2>执行时间轴</h2></div>{timeline}</section>
<section><div class="section-title"><span>TEAM</span><h2>{e(fixed["team_title"])}</h2></div><div class="grid">{"".join(f"<article><p>{e(x)}</p></article>" for x in fixed["team"])}</div></section>
<section class="materials"><div class="section-title"><span>NEXT STEP</span><h2>启动所需资料</h2></div><ul>{materials}</ul></section></main></body></html>'''.replace(
        '@media print{body{background:white}header,section,article,table{break-inside:avoid}}',
        '@media print{body{background:white}.overview{grid-template-columns:1fr 1.25fr}.risk-grid,.grid{grid-template-columns:repeat(2,1fr)}.page-two{break-before:page}article,table{break-inside:avoid}section{break-inside:auto}}'
    )


def internal_html(data, fixed, warnings):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>body{{font-family:-apple-system,"PingFang SC",sans-serif;max-width:1000px;margin:40px auto;line-height:1.6}}section{{border:1px solid #d9e5f2;padding:18px;margin:12px 0}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #d9e5f2;padding:7px}}.warning{{background:#fff7df}}</style></head><body><h1>DP内部审核附件</h1><section><b>合同：</b>{e(data.get("contract", "D01"))}<br><b>报价状态：</b>{e(data.get("quote_status", "待DP报价Skill返回"))}</section><section class="warning"><h2>预警与待确认</h2><p>{e(WARNING_PREFIX)}</p><ul>{items(warnings) or '<li>无</li>'}</ul></section><section><h2>课程工作量核查</h2>{table(("代码","课程","考核","工作量及依据","匹配服务"), course_rows(data, True))}</section><section><h2>范围边界</h2><ul>{items(fixed["scope_boundary"])}</ul></section></body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_html")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parent.parent
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    fixed = json.loads((skill / "assets/templates/dp_fixed_value_modules.json").read_text(encoding="utf-8"))
    from validate_intake import validate
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid intake: " + ", ".join(errors))
    warnings = warnings_for(data)
    output = Path(args.output_html)
    output.write_text(client_html(data, fixed), encoding="utf-8")
    Path(str(output) + ".internal.html").write_text(internal_html(data, fixed, warnings), encoding="utf-8")
    Path(str(output) + ".internal.json").write_text(json.dumps({"contract": data.get("contract", "D01"), "warnings": warnings, "quote_status": data.get("quote_status"), "rule": "Internal-only. Never merge this file into a client proposal."}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output_html)


if __name__ == "__main__":
    main()
