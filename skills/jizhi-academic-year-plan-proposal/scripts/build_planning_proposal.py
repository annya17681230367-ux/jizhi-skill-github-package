#!/usr/bin/env python3
"""Render a clean client proposal plus a separate internal audit artifact."""

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path

WARNING_PREFIX = "亲爱的学业规划师，您好！此次方案生成存在【预警提示】："


def e(value):
    return html.escape(str(value or ""))


def asset_uri(path):
    if not path.exists():
        return ""
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def items(values):
    return "".join(f"<li>{e(value)}</li>" for value in values if value)


def table(headers, rows, cls=""):
    head = "".join(f"<th>{e(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{e(x)}</td>" for x in row) + "</tr>" for row in rows)
    return f'<table class="{e(cls)}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def derive_warnings(data):
    warnings = list(data.get("warnings", [])) + list(data.get("pending", []))
    for course in data.get("courses", []):
        if course.get("workload_basis") in {"model_estimate", "pending"}:
            warnings.append(f"{course.get('code', '未知课程')}课程工作量尚未由官方资料核实")
        if not course.get("workload"):
            warnings.append(f"{course.get('code', '未知课程')}课程工作量待确认")
    return list(dict.fromkeys(x for x in warnings if x))


def course_rows(data, internal=False):
    rows = []
    for course in data.get("courses", []):
        workload = course.get("workload") or "待课程文件确认"
        if internal and course.get("workload_basis") == "model_estimate":
            workload += "（模型估算，需人工审核）"
        rows.append((course.get("code"), course.get("name"), course.get("assessment"), workload, course.get("service")))
    return rows


def profile_cards(data, labels):
    modules = data.get("planning_items", {})
    return "".join(f'<article><h3>{e(label)}</h3><p>{e(modules.get(label, "待补充"))}</p></article>' for label in labels)


def timeline_rows(data):
    return [(x.get("stage"), x.get("period", x.get("date")), x.get("action"), x.get("owner")) for x in data.get("timeline", [])]


def quote_client(data):
    quote = data.get("quote", {})
    rows = [
        (
            x.get("label"),
            x.get("quantity"),
            x.get("original", "按报价汇总"),
            x.get("discount", "按报价汇总"),
            x.get("final", "按报价汇总"),
        )
        for x in quote.get("lines", [])
    ]
    if not rows and not quote.get("final_total"):
        return ""
    catalog_rows = [
        (
            x.get("label"),
            f'专业课{x.get("specialist_lessons")}节+陪跑课{x.get("planning_lessons")}节',
            x.get("component_original"),
            x.get("standard_price"),
            x.get("savings"),
        )
        for x in quote.get("standard_catalog", [])
    ]
    catalog = ""
    if catalog_rows:
        selected = quote.get("selected_combo", {})
        selected_note = (
            f'{selected.get("key_courses", 0)}门重点+{selected.get("non_key_courses", 0)}门非重点'
            f'（{"已命中标准组合" if selected.get("matrix_matched") else "未命中标准组合，折后价需人工审核"}）'
        )
        catalog = f'''<div class="section-title"><span>PRICE GUIDE</span><h2>报价速查目录与资料</h2></div>
        <p class="quote-note">当前组合：{e(selected_note)}</p>
        {table(("标准组合", "课时配置", "组件单买价", "标准方案价", "节省"), catalog_rows, "quote-catalog")}'''
    return f'''<section class="quote"><div class="section-title"><span>QUOTE</span><h2>服务报价</h2></div>
    {table(("项目", "数量", "原价", "折扣", "折后价"), rows)}
    <div class="quote-total"><small>原价</small><s>{e(quote.get("original_total", "待核价"))}</s><small>折后价</small><strong>{e(quote.get("final_total", "待核价"))}</strong></div>{catalog}</section>'''


def brand_header(data, logo, ip):
    logo_html = f'<img class="logo" src="{logo}" alt="">' if logo and data.get("contract") != "T02" else ""
    ip_html = f'<img class="ip-hero" src="{ip}" alt="极致AI学业规划IP形象">' if ip else ""
    tags = [data.get("degree_level"), data.get("target_period"), f"目标：{data.get('target')}" if data.get("target") else ""]
    return f'''<header>{logo_html}<div class="header-copy"><div class="eyebrow">ACADEMIC PLANNING</div>
    <h1>{e(data.get("school"))}<br><em>{e(data.get("program"))}</em></h1><div class="tags">{"".join(f'<span>{e(x)}</span>' for x in tags if x)}</div></div>{ip_html}</header>'''


def execution_band(fixed, include_team):
    rhythm = (("每日", fixed["daily"]), ("每周", fixed["weekly"]), ("每月", fixed["monthly"]))
    cards = "".join(f'<article><h3>{e(k)}</h3><p>{e(v)}</p></article>' for k, v in rhythm)
    team = f'<div class="team"><h3>配套团队</h3><ul>{items(fixed["roles"])}</ul></div>' if include_team else ""
    return f'''<section class="service-band"><div class="section-title light"><span>TRACKABLE EXECUTION</span><h2>{e(fixed["ai_title"])}</h2></div><p class="lead">{e(fixed["ai_positioning"])}</p><div class="rhythm">{cards}</div>{team}</section>'''


def proposal_value_band(fixed):
    cards = "".join(
        f'<article><div class="value-card-head"><span>{index:02d}</span><h3>{e(item["title"])}</h3></div><p class="value-lead">{e(item["lead"])}</p><ul>{items(item["points"])}</ul></article>'
        for index, item in enumerate(fixed["proposal_values"], 1)
    )
    flow = "".join(f'<span>{e(label)}</span>' for label in ("诊断", "规划", "执行", "反馈", "调整"))
    return f'''<section class="proposal-values"><div class="section-title"><span>VALUE SYSTEM</span><h2>五大支持体系</h2></div><p class="value-intro">从目标诊断到持续执行，让学习过程有方向、有反馈、可调整。</p><div class="value-grid">{cards}</div><div class="value-flow"><b>持续闭环</b>{flow}</div></section>'''


def client_body(data, fixed, contracts, logo, ip):
    contract = data.get("contract", "T01")
    out = brand_header(data, logo, ip)
    profile = data.get("student_profile", [])
    courses = table(("课程代码", "课程名称", "考核形式", "工作量", "匹配服务"), course_rows(data), "course-table")
    timeline = table(("阶段", "时间", "核心行动", "负责角色"), timeline_rows(data), "timeline-table")
    if contract == "T00":
        out += f'<section><div class="section-title"><span>PROFILE</span><h2>学生情况</h2></div><ul>{items(profile)}</ul></section>'
        out += f'<section><div class="section-title"><span>REPORT</span><h2>个性化学业规划报告</h2></div><div class="grid">{profile_cards(data, fixed["eight_items"])}</div></section>'
        out += f'<section class="page-two"><div class="section-title"><span>COURSE MATCH</span><h2>课程与服务匹配</h2></div>{courses}</section>'
    elif contract == "T01":
        out += f'<section class="overview"><div><div class="section-title"><span>STUDENT PROFILE</span><h2>学业画像与年度目标</h2></div><ul>{items(profile)}</ul></div><div class="metrics"><b>{len(data.get("courses", []))}<small>门课程</small></b><b>{len(data.get("timeline", []))}<small>执行阶段</small></b><b>全年<small>规划周期</small></b></div></section>'
        out += f'<section><div class="section-title"><span>SIX MODULES</span><h2>六大学业规划模块</h2></div><div class="grid six">{profile_cards(data, fixed["six_items"])}</div></section>'
        out += f'<section class="page-two"><div class="section-title"><span>COURSE MATCH</span><h2>课程与服务匹配</h2></div>{courses}</section>'
        out += f'<section><div class="section-title"><span>EXECUTION ROADMAP</span><h2>阶段执行路径</h2></div>{timeline}</section>'
        out += execution_band(fixed, include_team=True)
        out += proposal_value_band(fixed)
    elif contract == "T02":
        out += f'<section class="overview"><div><div class="section-title"><span>SERVICE MATCH</span><h2>课程考核与服务安排</h2></div><ul>{items(profile)}</ul></div></section>'
        out += f'<section><div class="section-title"><span>COURSE MATCH</span><h2>课程与服务匹配</h2></div>{courses}</section><section>{timeline}</section>' + execution_band(fixed, include_team=False)
    elif contract == "T03":
        out += f'<section><div class="section-title"><span>SERVICE LIST</span><h2>课程与服务匹配</h2></div>{courses}</section>' + quote_client(data)
    elif contract == "T05":
        out += f'<section><div class="section-title"><span>PRODUCT SPLIT</span><h2>DP与学业规划服务分工</h2></div><div class="split"><article><h3>DP服务</h3><p>负责已确认的写作、报告、展示与项目任务管理。</p></article><article><h3>学业规划与陪跑</h3><p>负责课程理解、考试训练、周执行与学习轨迹管理。</p></article></div></section>'
        out += f'<section><div class="section-title"><span>COURSE MATCH</span><h2>课程与服务匹配</h2></div>{courses}</section><section>{timeline}</section>' + quote_client(data)
    return out


def client_html(data, fixed, contracts, logo, ip):
    body = client_body(data, fixed, contracts, logo, ip)
    contract = data.get("contract", "T01")
    template = contracts[contract]["fixed_case"]
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(data.get("school"))}学业规划方案</title><style>
@page{{size:A4;margin:0}}*{{box-sizing:border-box}}:root{{--navy:#082f6b;--blue:#0765f5;--cyan:#0bc8b5;--ice:#eef7ff;--line:#cce1f5;--ink:#17243c}}body{{margin:0;background:#dcecff;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.55;letter-spacing:0}}main{{width:210mm;margin:auto;background:#fff;min-height:297mm}}header{{position:relative;min-height:89mm;padding:16mm 15mm 13mm;background:linear-gradient(120deg,#f5faff 0%,#eef8ff 62%,#dffcf7 100%);border-bottom:1px solid var(--line)}}.header-copy{{position:relative;z-index:1;max-width:126mm}}.logo{{width:47mm;height:auto;display:block;margin-bottom:12mm;object-fit:contain}}.ip-hero{{position:absolute;right:13mm;bottom:10mm;width:43mm;height:43mm;display:block;object-fit:contain;object-position:center}}.contract-T05 header{{min-height:70mm;padding-top:10mm;padding-bottom:8mm}}.contract-T05 .logo{{width:40mm;margin-bottom:5mm}}.contract-T05 .ip-hero{{right:14mm;bottom:7mm;width:34mm;height:34mm}}.contract-T05 h1{{font-size:25px}}.eyebrow,.section-title span{{font-size:10px;font-weight:800;letter-spacing:1.2px;color:#078b7d}}h1{{margin:5px 0 9px;color:var(--navy);font-size:31px;line-height:1.2}}h1 em{{font-style:normal;color:var(--blue)}}.tags{{display:flex;gap:7px;flex-wrap:wrap;max-width:122mm}}.tags span{{padding:4px 9px;border:1px solid #bfe0ff;border-radius:5px;background:white;color:#315477;font-size:11px}}section{{padding:8mm 15mm;border-bottom:1px solid #e5eef8}}.section-title{{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}}h2{{margin:0;color:var(--navy);font-size:20px;line-height:1.25}}h3{{margin:0 0 5px;color:var(--navy);font-size:14px}}p,li{{font-size:12px}}ul{{margin:6px 0;padding-left:18px}}.overview{{display:grid;grid-template-columns:1.45fr 1fr;gap:18px}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;align-self:center}}.metrics b{{padding:12px 6px;text-align:center;color:var(--blue);font-size:24px;border:1px solid var(--line);border-radius:6px}}.metrics small{{display:block;color:#60748c;font-size:9px}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}}.grid.six{{grid-template-columns:repeat(3,1fr)}}article{{padding:11px;border:1px solid var(--line);border-radius:6px;background:#fbfdff}}article p{{margin:0;color:#5c6f87}}table{{width:100%;border-collapse:separate;border-spacing:0;font-size:10px;border:1px solid var(--line);border-radius:6px;overflow:hidden}}th,td{{padding:7px 8px;text-align:left;vertical-align:top;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}}th:last-child,td:last-child{{border-right:0}}tr:last-child td{{border-bottom:0}}th{{color:var(--navy);background:#eaf5ff;font-weight:700}}.course-table th:nth-child(1){{width:12%}}.course-table th:nth-child(2){{width:17%}}.course-table th:nth-child(3){{width:25%}}.course-table th:nth-child(4){{width:18%}}.service-band{{color:white;background:linear-gradient(110deg,#075be6,#0abdaf)}}.service-band h2,.service-band h3,.service-band .section-title span{{color:white}}.service-band .lead{{font-size:14px;font-weight:700}}.rhythm{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}.service-band article{{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.26)}}.service-band article p{{color:white}}.team ul{{display:grid;grid-template-columns:repeat(2,1fr);gap:3px 18px}}.proposal-values{{break-before:page;min-height:297mm;padding:15mm;background:linear-gradient(145deg,#f2f8ff 0%,#e8fffb 100%);display:flex;flex-direction:column}}.proposal-values .section-title{{margin-bottom:4px}}.value-intro{{margin:0 0 14px;color:#49647f;font-size:12px}}.value-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:11px;flex:1}}.value-grid article{{border-top:5px solid var(--cyan);background:#fff;box-shadow:0 5px 14px rgba(8,47,107,.06);padding:14px 15px}}.value-grid article:first-child{{grid-column:span 2;border-top-color:var(--blue)}}.value-grid article:nth-child(2){{border-top-color:var(--blue)}}.value-card-head{{display:flex;align-items:center;gap:9px;margin-bottom:6px}}.value-card-head span{{display:grid;place-items:center;width:25px;height:25px;border-radius:50%;color:#fff;background:var(--cyan);font-size:10px;font-weight:800}}.value-grid article:nth-child(-n+2) .value-card-head span{{background:var(--blue)}}.value-grid h3{{margin:0;font-size:14px}}.value-lead{{font-size:11px!important;line-height:1.45!important;color:#24486e!important;font-weight:700}}.value-grid ul{{margin:7px 0 0;padding-left:17px;color:#5b6f86}}.value-grid li{{font-size:10px;line-height:1.55;margin:2px 0}}.value-flow{{margin-top:14px;padding:11px 13px;border-radius:6px;color:#fff;background:linear-gradient(100deg,var(--blue),var(--cyan));display:flex;align-items:center;justify-content:space-between;gap:7px}}.value-flow b{{font-size:12px}}.value-flow span{{padding:5px 12px;border:1px solid rgba(255,255,255,.38);border-radius:4px;font-size:10px;font-weight:700}}.split{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.split article:first-child{{border-top:5px solid var(--blue)}}.split article:last-child{{border-top:5px solid var(--cyan)}}.quote-total{{display:flex;justify-content:flex-end;align-items:baseline;gap:10px;margin-top:14px;color:#50627a}}.quote-total strong{{font-size:26px;color:var(--blue)}}@media(max-width:760px){{main{{width:100%}}.overview,.grid.six,.grid,.split,.rhythm,.value-grid{{grid-template-columns:1fr}}.value-grid article:first-child{{grid-column:span 1}}.metrics{{grid-template-columns:repeat(3,1fr)}}.ip-hero{{position:static;width:38mm;height:38mm;margin:8mm 0 0 auto}}}}@media print{{body{{background:white}}main{{width:100%}}header,section,article,table{{break-inside:avoid}}}}
</style></head><body><main class="contract-{e(contract)}" data-fixed-template="{e(template)}">{body}</main></body></html>'''.replace(
        '@media print{body{background:white}main{width:100%}header,section,article,table{break-inside:avoid}}',
        '@media print{body{background:white}main{width:100%}.overview{grid-template-columns:1.45fr 1fr}.grid{grid-template-columns:repeat(2,1fr)}.grid.six{grid-template-columns:repeat(3,1fr)}.split{grid-template-columns:1fr 1fr}.rhythm{grid-template-columns:repeat(3,1fr)}.value-grid{grid-template-columns:repeat(2,1fr)}.value-grid article:first-child{grid-column:span 2}.page-two{break-before:page}article,table{break-inside:avoid}section{break-inside:auto}}'
    )


def internal_html(data, fixed, contracts, warnings):
    sources = [(x.get("label"), x.get("url"), x.get("source_year"), x.get("verified_at")) for x in data.get("sources", [])]
    quote = data.get("quote", {})
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>body{{font-family:-apple-system,"PingFang SC",sans-serif;max-width:1000px;margin:40px auto;line-height:1.6;color:#17243c}}h1{{color:#082f6b}}section{{border:1px solid #d9e5f2;padding:18px;margin:12px 0}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #d9e5f2;padding:7px;text-align:left}}.warning{{background:#fff7df}}</style></head><body><h1>内部审核附件</h1>
    <section><b>合同：</b>{e(data.get("contract"))} / {e(contracts[data.get("contract", "T01")]["label"])}<br><b>客户文件：</b>不得包含本附件内容</section>
    <section class="warning"><h2>预警与待确认</h2><p>{e(WARNING_PREFIX)}</p><ul>{items(warnings) or '<li>无</li>'}</ul></section>
    <section><h2>课程与服务匹配核查</h2>{table(("代码","课程","考核","工作量及依据","服务"), course_rows(data, True))}</section>
    <section><h2>官方来源</h2>{table(("来源","网址","资料年份","核验日期"), sources)}</section>
    <section><h2>报价审核</h2><p>追溯ID：{e(quote.get("trace_id", "待生成"))}　审核状态：{e(quote.get("review_status", "待审核"))}</p><p>{e(fixed["disclaimer"])}</p></section></body></html>'''


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
    logo = asset_uri(skill / "assets/brand/full-logo.jpg")
    ip_files = {"T00": "report-scroll.jpg", "T01": "study-dashboard.jpg", "T05": "research-files.jpg"}
    ip = asset_uri(skill / "assets/ip" / ip_files[data.get("contract", "T01")]) if data.get("contract", "T01") in ip_files else ""
    output.write_text(client_html(data, fixed, contracts, logo, ip), encoding="utf-8")
    internal_json = {"contract": data.get("contract", "T01"), "warnings": warnings, "sources": data.get("sources", []), "quote_audit": data.get("quote", {}), "rule": "Internal-only. Never merge this file into a client proposal."}
    Path(str(output) + ".internal.html").write_text(internal_html(data, fixed, contracts, warnings), encoding="utf-8")
    Path(str(output) + ".internal.json").write_text(json.dumps(internal_json, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output_html)


if __name__ == "__main__":
    main()
