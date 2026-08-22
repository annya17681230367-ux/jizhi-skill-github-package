#!/usr/bin/env python3
"""Render a stable six-module DP proposal HTML from structured JSON."""

import argparse
import html
import json
from pathlib import Path

WARNING_PREFIX = "亲爱的学业规划师，您好！此次方案生成存在【预警提示】："


def esc(value):
    return html.escape(str(value or ""))


def cards(items, class_name="card"):
    return "".join(
        f'<article class="{class_name}"><h3>{esc(item.get("title"))}</h3>'
        f'<p>{esc(item.get("detail"))}</p></article>'
        for item in items
    )


def rows(items, fields):
    output = []
    for item in items:
        output.append("<tr>" + "".join(f"<td>{esc(item.get(field))}</td>" for field in fields) + "</tr>")
    return "".join(output)


def fixed_list(title, items):
    content = "".join(f"<li>{esc(item)}</li>" for item in items)
    return f'<section><h2>{esc(title)}</h2><ul class="fixed-list">{content}</ul></section>'


def render(data, fixed):
    warnings = list(data.get("warnings", []))
    for course in data.get("courses", []):
        if course.get("workload_basis") in {"model_estimate", "pending"} or not course.get("workload"):
            warnings.append(f"{course.get('code', '未知课程')}课程工作量需人工确认")
    warnings = list(dict.fromkeys(x for x in warnings if x))
    risks = cards(data.get("risks", []), "card risk")
    course_rows = rows(
        data.get("courses", []),
        ("name", "code", "assessment", "workload", "service_focus"),
    )
    timeline_rows = rows(
        data.get("timeline", []),
        ("stage", "date", "action", "student_input"),
    )
    materials = "".join(f"<li>{esc(item)}</li>" for item in data.get("materials_required", []))
    situation = "".join(f"<p>{esc(item)}</p>" for item in data.get("situation", []))
    core_value = fixed_list(fixed["core_value_title"], fixed["core_value"])
    assurance = fixed_list(fixed["assurance_process_title"], fixed["assurance_process"])
    team = fixed_list(fixed["team_title"], fixed["team"])
    boundary = fixed_list("服务范围边界", fixed["scope_boundary"])
    warning_html = ""
    if warnings:
        warning_html = f'<section class="warning"><h2>预警提示</h2><p><b>{esc(WARNING_PREFIX)}</b></p><ul>{"".join(f"<li>{esc(x)}</li>" for x in warnings)}</ul></section>'
    contract = data.get("contract", "D01")
    situation_html = "" if contract == "D02" else f'<section><h2>你的情况</h2>{situation}</section><section><h2>核心风险</h2><div class="grid">{risks}</div></section>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(data.get('school'))} {esc(data.get('program'))} DP方案</title>
<style>
:root{{--ink:#0d1b3e;--blue:#005cff;--cyan:#3bdbbd;--paper:#f7faff;--line:#dce7f5;--muted:#667085}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6}}
main{{max-width:1080px;margin:auto;background:#fff}} header,section{{padding:34px 44px;border-bottom:1px solid var(--line)}}
header{{background:#eef6ff}} h1{{font-size:34px;line-height:1.25;margin:12px 0}} h2{{font-size:22px;margin:0 0 18px}} h3{{font-size:16px;margin:0 0 8px}}
.eyebrow{{color:#087f78;font-weight:700}} .tags{{display:flex;gap:8px;flex-wrap:wrap}} .tag{{padding:5px 10px;background:#e8f1ff;border-radius:6px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}} .card{{border:1px solid var(--line);padding:16px;border-radius:8px;background:#fff}}
.risk{{border-top:4px solid #f59e0b}} table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{padding:10px;border:1px solid var(--line);text-align:left;vertical-align:top}} th{{background:#eef6ff}}
.fixed-list{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:0;list-style:none}} .fixed-list li{{padding:12px;border-left:4px solid var(--cyan);background:#f3fffd}}
.quote{{font-size:24px;font-weight:700;color:var(--blue)}} footer{{padding:24px 44px;color:var(--muted);font-size:12px}}
@media(max-width:760px){{header,section{{padding:24px 20px}}.grid,.fixed-list{{grid-template-columns:1fr}}table{{font-size:12px}}}}
    .warning{{background:#fff8e8;border-left:5px solid #f59e0b}} @media print{{body{{background:#fff}}main{{max-width:none}}section,table,.card{{break-inside:avoid}}}}
</style>
</head>
<body><main>
<header>
  <div class="eyebrow">DP ACADEMIC SUPPORT</div>
  <h1>{esc(data.get('school'))}<br>{esc(data.get('program'))} DP服务方案</h1>
  <div class="tags"><span class="tag">{esc(data.get('target_year'))}</span><span class="tag">目标：{esc(data.get('target_score'))}</span><span class="tag">{esc(data.get('product'))}</span><span class="tag">范围：{esc(data.get('scope'))}</span></div>
</header>
{situation_html}
<section><h2>课程与服务匹配</h2><table><thead><tr><th>课程名称</th><th>课程代码</th><th>课程考核形式</th><th>课程工作量</th><th>匹配服务</th></tr></thead><tbody>{course_rows}</tbody></table></section>
{core_value}{assurance}
<section><h2>执行时间轴</h2><table><thead><tr><th>阶段</th><th>时间</th><th>执行动作</th><th>学生需提供</th></tr></thead><tbody>{timeline_rows}</tbody></table></section>
{team}{boundary}
<section><h2>报价状态与下一步</h2><p class="quote">{esc(data.get('quote_status', '待报价确认'))}</p><ul>{materials}</ul></section>
{warning_html}
<footer>最终执行以学生提供的最新brief、rubric、课程平台信息和学校要求为准。</footer>
</main></body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_html")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    fixed_path = skill_dir / "assets" / "templates" / "dp_fixed_value_modules.json"
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    fixed = json.loads(fixed_path.read_text(encoding="utf-8"))
    from validate_intake import validate
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid intake: " + ", ".join(errors))
    Path(args.output_html).write_text(render(data, fixed), encoding="utf-8")
    warnings = list(data.get("warnings", []))
    for course in data.get("courses", []):
        if course.get("workload_basis") in {"model_estimate", "pending"} or not course.get("workload"):
            warnings.append(f"{course.get('code', '未知课程')}课程工作量需人工确认")
    Path(args.output_html + ".warnings.json").write_text(json.dumps({"prefix": WARNING_PREFIX, "warnings": list(dict.fromkeys(warnings))}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output_html)


if __name__ == "__main__":
    main()
