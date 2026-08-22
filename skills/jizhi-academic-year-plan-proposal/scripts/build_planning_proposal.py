#!/usr/bin/env python3
"""Build stable annual-planning HTML from the canonical intake JSON."""

import argparse
import html
import json
from pathlib import Path


def e(value):
    return html.escape(str(value or ""))


def list_items(items):
    return "".join(f"<li>{e(item)}</li>" for item in items)


def render(data, fixed):
    courses = "".join(
        "<tr>" + "".join(f"<td>{e(course.get(key))}</td>" for key in ("code", "name", "assessment", "priority", "service", "hours")) + "</tr>"
        for course in data["courses"]
    )
    timeline = "".join(
        "<tr>" + "".join(f"<td>{e(item.get(key))}</td>" for key in ("stage", "period", "action", "owner")) + "</tr>"
        for item in data.get("timeline", [])
    )
    sources = "".join(f'<li><a href="{e(x.get("url"))}">{e(x.get("label"))}</a></li>' for x in data.get("sources", []))
    six = "".join(f"<article><b>{e(title)}</b><p>{e(data.get('planning_items', {}).get(title, '待补充'))}</p></article>" for title in fixed["six_items"])
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{e(data['school'])}学业规划</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#eef6ff;color:#092d66;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;line-height:1.55}}main{{max-width:1080px;margin:auto;background:white}}header,section{{padding:30px 42px;border-bottom:1px solid #dce9f7}}h1{{font-size:34px}}h2{{font-size:22px}}.tags{{display:flex;gap:8px;flex-wrap:wrap}}.tags span{{background:#e6fffa;padding:5px 10px;border-radius:5px}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}article{{border:1px solid #cfe0f5;padding:14px;border-radius:8px}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #cfe0f5;padding:9px;text-align:left;vertical-align:top}}th{{background:#eaf4ff}}.ai{{background:#edfffb;border-left:5px solid #08bda8}}@media(max-width:760px){{header,section{{padding:22px 18px}}.grid{{grid-template-columns:1fr}}}}@media print{{body{{background:white}}section,table,article{{break-inside:avoid}}}}
</style></head><body><main><header><p>ACADEMIC PLANNING · {e(data.get('contract','T01'))}</p><h1>{e(data['school'])}<br>{e(data['program'])} 学业规划方案</h1><div class="tags"><span>{e(data['degree_level'])}</span><span>{e(data['target_period'])}</span><span>目标：{e(data['target'])}</span></div></header>
<section><h2>学生基础</h2><ul>{list_items(data['student_profile'])}</ul></section><section><h2>六大学业规划模块</h2><div class="grid">{six}</div></section>
<section><h2>课程考核与服务匹配</h2><table><thead><tr><th>代码</th><th>课程</th><th>考核</th><th>优先级</th><th>服务</th><th>课时</th></tr></thead><tbody>{courses}</tbody></table></section>
<section><h2>阶段时间轴</h2><table><thead><tr><th>阶段</th><th>时间</th><th>行动</th><th>负责人</th></tr></thead><tbody>{timeline}</tbody></table></section>
<section><h2>每日 / 每周 / 每月执行</h2><ul><li>{e(fixed['daily'])}</li><li>{e(fixed['weekly'])}</li><li>{e(fixed['monthly'])}</li></ul></section>
<section class="ai"><h2>{e(fixed['ai_title'])}</h2><p><b>{e(fixed['ai_positioning'])}</b></p><ul>{list_items(fixed['ai_functions'])}</ul></section>
<section><h2>配套团队</h2><ul>{list_items(fixed['roles'])}</ul></section><section><h2>来源与待确认</h2><ul>{sources}{list_items(data.get('pending', []))}</ul><p>{e(fixed['disclaimer'])}</p></section>
</main></body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_html")
    args = parser.parse_args()
    skill = Path(__file__).resolve().parent.parent
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    fixed = json.loads((skill / "assets/templates/planning_fixed_modules.json").read_text(encoding="utf-8"))
    from validate_intake import validate
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid intake: " + ", ".join(errors))
    Path(args.output_html).write_text(render(data, fixed), encoding="utf-8")
    print(args.output_html)


if __name__ == "__main__":
    main()
