#!/usr/bin/env python3
"""Build a branded client-facing academic support proposal HTML."""

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path


def esc(value):
    return html.escape(str(value or ""))


def asset_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())


def validate(data):
    errors = []
    required = ["student", "targets", "lesson_plan", "roles", "courses", "roadmap", "tracking"]
    for key in required:
        if key not in data:
            errors.append(f"missing {key}")
    if errors:
        return errors

    lesson_plan = data["lesson_plan"]
    professional = int(lesson_plan.get("professional_lessons", 0))
    pacing = int(lesson_plan.get("pacing_lessons", 0))
    total = int(lesson_plan.get("total_lessons", 0))
    if professional + pacing != total:
        errors.append("professional_lessons + pacing_lessons must equal total_lessons")
    if professional <= pacing:
        errors.append("professional_lessons should be greater than pacing_lessons for professional-first plans")

    cap = int(lesson_plan.get("per_course_cap", 0))
    for idx, course in enumerate(data["courses"], 1):
        course_total = int(course.get("professional_lessons", 0)) + int(course.get("pacing_lessons", 0))
        if cap and course_total > cap:
            errors.append(f"course {idx} exceeds per_course_cap")
        if int(course.get("pacing_lessons", 0)) > 3:
            errors.append(f"course {idx} has more than 3 pacing lessons")
    return errors


def role_card(role):
    return f"<div class='role'><h3>{esc(role.get('title'))}</h3><p>{esc(role.get('text'))}</p></div>"


def small_stat(value, label, note=""):
    return f"<div class='mini'><b>{esc(value)}</b><span>{esc(label)}</span><small>{esc(note)}</small></div>"


def course_card(course, idx):
    risk = course.get("risk", "")
    risk_class = "high" if "高" in risk else ("low" if "低" in risk else "mid")
    lessons = f"专业课 {course.get('professional_lessons')} 节 + 陪跑课 {course.get('pacing_lessons')} 节"
    return f"""
    <article class="course {risk_class}">
      <div class="course-num">{idx:02d}</div>
      <div>
        <h3>{esc(course.get('name'))}</h3>
        <p class="cn">{esc(course.get('cn'))}</p>
      </div>
      <div class="risk">风险 {esc(risk)}</div>
      <div class="line"><b>重点观察</b><span>{esc(course.get('watch'))}</span></div>
      <div class="line"><b>服务配置</b><span>{esc(lessons)}</span></div>
      <div class="line"><b>课程支持</b><span>{esc(course.get('support'))}</span></div>
    </article>
    """


def roadmap_step(item):
    return f"""
    <div class="step">
      <b>{esc(item.get('label'))}</b>
      <div><h3>{esc(item.get('title'))}</h3><p>{esc(item.get('text'))}</p></div>
      <p>{esc(item.get('owner'))}</p>
    </div>
    """


def tracking_item(item):
    return f"<div class='check'><b>{esc(item.get('title'))}</b>{esc(item.get('text'))}</div>"


def build_html(data, skill_dir):
    assets = skill_dir / "assets"
    logo = asset_uri(assets / "brand/full-logo.jpg")
    ip_study = asset_uri(assets / "ip/study-dashboard.jpg")
    ip_exam = asset_uri(assets / "ip/pass-test.jpg")
    ip_grad = asset_uri(assets / "ip/graduation.jpg")

    student = data["student"]
    targets = data["targets"]
    lesson = data["lesson_plan"]
    professional = int(lesson["professional_lessons"])
    pacing = int(lesson["pacing_lessons"])
    total = int(lesson["total_lessons"])
    prof_pct = round(professional / total * 100)
    pacing_pct = 100 - prof_pct
    tiers = lesson.get("tiers", [])

    profile_cards = "".join(
        f"<div class='summary-card'><b>{esc(item.get('value'))}</b><h3>{esc(item.get('label'))}</h3><p>{esc(item.get('note'))}</p></div>"
        for item in student.get("profile", [])
    )
    if not profile_cards:
        profile_cards = (
            f"<div class='summary-card'><b>{esc(student.get('entry_date'))}</b><h3>新生入学</h3><p>开学前完成课程资料建档。</p></div>"
            f"<div class='summary-card'><b>{len(data['courses'])}</b><h3>课程数量</h3><p>按课程风险分层匹配服务。</p></div>"
            f"<div class='summary-card'><b>{esc(targets.get('main'))}</b><h3>年度主目标</h3><p>以稳定通过为底线，优势课程争取突破。</p></div>"
        )
    tier_stats = "".join(small_stat(t.get("value"), t.get("label"), t.get("note")) for t in tiers)
    roles = "".join(role_card(x) for x in data["roles"])
    high_courses = [c for c in data["courses"] if "高" in c.get("risk", "")]
    other_courses = [c for c in data["courses"] if "高" not in c.get("risk", "")]
    high_cards = "".join(course_card(c, i + 1) for i, c in enumerate(high_courses))
    other_cards = "".join(course_card(c, i + 1 + len(high_courses)) for i, c in enumerate(other_courses))
    roadmap = "".join(roadmap_step(x) for x in data["roadmap"])
    tracking = "".join(tracking_item(x) for x in data["tracking"])
    materials = "、".join(data.get("materials_needed", []))
    boundary = data.get("boundary_note") or "正式课程名可在拿到课表和 syllabus 后替换。"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{esc(student.get('program'))} 学业护航方案</title>
<style>
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; }}
:root {{ --blue:#005CFF; --cyan:#00EAD3; --purple:#8473FF; --yellow:#FFDE55; --ink:#071C3F; --soft:#F4F8FF; --line:#D7E5FF; --muted:#5B6F8F; }}
body {{ margin:0; background:#eaf2ff; color:var(--ink); font-family:"Source Han Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif; letter-spacing:0; }}
.page {{ width:210mm; height:297mm; margin:0 auto; background:#fff; position:relative; overflow:hidden; page-break-after:always; padding:18mm; }}
.page:last-child {{ page-break-after:auto; }}
.logo {{ width:44mm; height:auto; object-fit:contain; display:block; }}
.cover {{ padding:0; background:linear-gradient(135deg,#f6faff 0%,#e9f3ff 64%,#dffffb 100%); }}
.cover-grid {{ display:grid; grid-template-columns:1.05fr .95fr; height:100%; }}
.cover-left {{ padding:22mm 0 20mm 18mm; position:relative; z-index:2; }}
.cover .logo {{ margin-bottom:28mm; }}
.kicker {{ color:#008f83; font-family:Montserrat,"Avenir Next",Arial,sans-serif; font-size:12px; font-weight:800; letter-spacing:2.6px; text-transform:uppercase; }}
h1 {{ margin:7mm 0; font-size:38px; line-height:1.12; color:var(--ink); font-weight:800; }}
h1 span {{ color:var(--blue); display:block; }}
.cover-copy {{ font-size:17px; line-height:1.8; color:#284466; max-width:118mm; }}
.cover-meta {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12mm; }}
.cover-meta span {{ padding:7px 10px; border:1px solid #b8d1ff; border-radius:7px; background:#fff; color:#1f4778; font-size:12px; font-weight:600; }}
.cover-right {{ position:relative; background:var(--blue); }}
.cover-right:before {{ content:""; position:absolute; left:-35mm; top:0; bottom:0; width:70mm; background:#e9f3ff; transform:skewX(-4deg); transform-origin:bottom left; }}
.cover-right:after {{ content:""; position:absolute; right:-35mm; bottom:-25mm; width:100mm; height:100mm; border-radius:50%; background:var(--cyan); opacity:.95; }}
.ip-cover {{ position:absolute; right:16mm; bottom:34mm; width:62mm; height:62mm; object-fit:contain; z-index:2; }}
.cover-block {{ position:absolute; top:34mm; right:18mm; z-index:2; color:#fff; text-align:right; font-family:Montserrat,"Avenir Next",Arial,sans-serif; }}
.cover-block b {{ display:block; font-size:50px; line-height:1; }}
.cover-block small {{ display:block; margin-top:5px; letter-spacing:1.6px; text-transform:uppercase; }}
.footer {{ position:absolute; left:18mm; right:18mm; bottom:10mm; display:flex; justify-content:space-between; align-items:center; color:#7890b2; font-size:10px; font-family:Montserrat,"Avenir Next",Arial,sans-serif; }}
.footer:before {{ content:""; position:absolute; left:0; right:0; top:-6mm; height:1px; background:#e1eaff; }}
.title-row {{ display:flex; justify-content:space-between; gap:20px; align-items:flex-start; margin-bottom:11mm; }}
.title-row .logo {{ width:36mm; margin-top:1mm; }}
h2 {{ margin:0; font-size:26px; line-height:1.22; font-weight:800; color:var(--ink); }}
.subtitle {{ color:var(--muted); font-size:13px; margin-top:5px; }}
.blue-band {{ background:var(--blue); color:#fff; border-radius:0 0 22mm 0; padding:14mm 16mm; margin:-18mm -18mm 10mm -18mm; }}
.blue-band h2,.blue-band .subtitle,.blue-band .kicker {{ color:#fff; }}
.summary-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:8mm; }}
.summary-card,.role,.mini,.course,.step,.check {{ border:1px solid var(--line); background:#fff; }}
.summary-card {{ min-height:42mm; border-radius:7px; padding:9mm; background:linear-gradient(180deg,#fff,#f8fbff); }}
.summary-card b {{ display:block; color:var(--blue); font-size:28px; line-height:1; font-family:Montserrat,"Avenir Next",Arial,sans-serif; margin-bottom:5mm; }}
.summary-card h3,.role h3 {{ margin:0 0 3mm; color:var(--ink); font-size:15px; }}
.summary-card p,.role p {{ margin:0; color:#526a8b; font-size:11px; line-height:1.65; }}
.service-map {{ display:grid; grid-template-columns:1fr 1fr; gap:7mm; margin-top:8mm; }}
.role {{ border-radius:8px; padding:7mm; min-height:40mm; position:relative; }}
.role:before {{ content:""; position:absolute; top:0; left:0; right:0; height:5px; background:var(--blue); border-radius:8px 8px 0 0; }}
.role:nth-child(even):before {{ background:var(--cyan); }}
.lesson-panel {{ background:#f7faff; border:1px solid var(--line); border-radius:10px; padding:10mm; margin-top:8mm; }}
.ratio {{ height:14mm; display:grid; grid-template-columns:{prof_pct}fr {pacing_pct}fr; border-radius:8px; overflow:hidden; margin:8mm 0 5mm; }}
.ratio div:first-child {{ background:var(--blue); }}
.ratio div:last-child {{ background:var(--cyan); }}
.ratio-label {{ display:flex; justify-content:space-between; font-size:15px; font-weight:800; color:#213b63; }}
.lesson-stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:5mm; margin-top:8mm; }}
.mini {{ border-radius:7px; padding:6mm; }}
.mini b {{ display:block; color:var(--blue); font-size:27px; font-family:Montserrat,"Avenir Next",Arial,sans-serif; }}
.mini span,.mini small {{ display:block; font-size:11px; color:#4a6283; line-height:1.55; }}
.course-layout {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; }}
.course {{ border-radius:8px; padding:6mm; min-height:67mm; display:grid; grid-template-columns:12mm 1fr auto; gap:3mm 5mm; break-inside:avoid; }}
.course.high {{ border-top:5px solid var(--blue); }}
.course.mid {{ border-top:5px solid var(--purple); }}
.course.low {{ border-top:5px solid var(--cyan); }}
.course-num {{ font-family:Montserrat,"Avenir Next",Arial,sans-serif; color:#8799b7; font-weight:800; font-size:15px; }}
.course h3 {{ margin:0; font-size:14px; line-height:1.25; color:var(--ink); }}
.course .cn {{ margin:1mm 0 0; color:#51698a; font-size:11px; }}
.risk {{ align-self:start; justify-self:end; padding:4px 8px; border-radius:20px; color:#06346f; background:#eaf4ff; font-weight:800; font-size:10px; white-space:nowrap; }}
.line {{ grid-column:2 / 4; display:grid; grid-template-columns:22mm 1fr; gap:3mm; font-size:10.4px; line-height:1.55; color:#4b6385; }}
.line b {{ color:#06346f; }}
.timeline {{ display:grid; gap:4mm; margin-top:6mm; }}
.step {{ display:grid; grid-template-columns:30mm 1fr 40mm; gap:5mm; border-radius:7px; padding:5mm; }}
.step b {{ color:var(--blue); font-family:Montserrat,"Avenir Next",Arial,sans-serif; }}
.step h3 {{ margin:0 0 2mm; font-size:14px; }}
.step p {{ margin:0; font-size:11px; color:#526a8b; line-height:1.55; }}
.ai-page {{ background:linear-gradient(135deg,#f6faff 0%,#eff7ff 60%,#e8fffb 100%); }}
.ai-wrap {{ display:grid; grid-template-columns:1.2fr .8fr; gap:12mm; align-items:center; }}
.ip-mid {{ width:58mm; height:58mm; object-fit:contain; display:block; margin:0 auto 8mm; }}
.checklist {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; }}
.check {{ border-radius:7px; padding:6mm; font-size:12px; color:#4b6385; line-height:1.7; }}
.check b {{ display:block; color:var(--ink); font-size:14px; margin-bottom:2mm; }}
.notice {{ margin-top:8mm; background:#fff8df; border:1px solid #ffe28c; border-radius:8px; padding:6mm; color:#6b581a; font-size:11px; line-height:1.7; }}
</style>
</head>
<body>
<main>
  <section class="page cover">
    <div class="cover-grid">
      <div class="cover-left">
        <img class="logo" src="{logo}" alt="">
        <div class="kicker">{esc(student.get('headline') or 'YEAR ONE SUPPORT')}</div>
        <h1>新生首年<br><span>学业护航方案</span></h1>
        <p class="cover-copy">面向 {esc(student.get('entry_date'))} 入学的 {esc(student.get('program'))}，围绕线下考试、专业基础和英文学习适应，配置专业课主导的全年支持。</p>
        <div class="cover-meta"><span>{esc(student.get('school'))}</span><span>{len(data['courses'])} 门课程</span><span>专业课 {professional} 节</span><span>陪跑课 {pacing} 节</span></div>
      </div>
      <div class="cover-right"><div class="cover-block"><b>{total}</b><small>Lessons / Year</small></div><img class="ip-cover" src="{ip_study}" alt=""></div>
    </div>
  </section>

  <section class="page">
    <div class="title-row"><div><div class="kicker">STUDENT CONTEXT</div><h2>首年学习判断</h2><p class="subtitle">底线：{esc(targets.get('baseline'))}；主目标：{esc(targets.get('main'))}；冲刺：{esc(targets.get('stretch'))}。</p></div><img class="logo" src="{logo}" alt=""></div>
    <div class="summary-grid">{profile_cards}</div>
    <div class="service-map">{roles}</div>
    <div class="footer"><span>JIZHI AI ACADEMIC SUPPORT</span><span>02</span></div>
  </section>

  <section class="page">
    <div class="blue-band"><div class="kicker">LESSON PLAN</div><h2>课时结构</h2><p class="subtitle">陪跑课控制在每门 2-3 节，其余集中给专业课。</p></div>
    <div class="lesson-panel"><div class="ratio"><div></div><div></div></div><div class="ratio-label"><span>专业课 {professional} 节 / {prof_pct}%</span><span>陪跑课 {pacing} 节 / {pacing_pct}%</span></div><div class="lesson-stats">{tier_stats}</div></div>
    <div class="service-map"><div class="role"><h3>专业课投放方向</h3><p>优先处理课程理解、考试题型、错题复盘和考前训练。</p></div><div class="role"><h3>陪跑课投放方向</h3><p>每门课只保留必要陪跑，用于建档、周任务、考试提醒和阶段复盘。</p></div><div class="role"><h3>考试前安排</h3><p>重点课程考前进入题型训练，常规课程完成框架复习与错题订正。</p></div><div class="role"><h3>动态调整</h3><p>开学第 4 周、每月、考前 4 周进行课程风险复盘。</p></div></div>
    <div class="footer"><span>PROFESSIONAL LESSONS FIRST</span><span>03</span></div>
  </section>

  <section class="page">
    <div class="title-row"><div><div class="kicker">COURSE RISK MAP</div><h2>课程风险与服务匹配</h2><p class="subtitle">{esc(boundary)}</p></div><img class="logo" src="{logo}" alt=""></div>
    <div class="course-layout">{high_cards}</div>
    <div class="footer"><span>HIGH RISK MODULES</span><span>04</span></div>
  </section>

  <section class="page">
    <div class="title-row"><div><div class="kicker">COURSE RISK MAP</div><h2>课程风险与服务匹配</h2><p class="subtitle">中风险课程重点控制框架、练习频率和考前清单。</p></div><img class="logo" src="{logo}" alt=""></div>
    <div class="course-layout">{other_cards}</div>
    <div class="footer"><span>REGULAR RISK MODULES</span><span>05</span></div>
  </section>

  <section class="page">
    <div class="title-row"><div><div class="kicker">SERVICE ROADMAP</div><h2>全年服务推进</h2><p class="subtitle">以开学、学期中、考前和成绩复盘四个节点管理。</p></div><img class="logo" src="{logo}" alt=""></div>
    <div class="timeline">{roadmap}</div>
    <div class="footer"><span>STAGE BASED SUPPORT</span><span>06</span></div>
  </section>

  <section class="page ai-page">
    <div class="title-row"><div><div class="kicker">TRACKABLE LEARNING</div><h2>过程沉淀与启动资料</h2><p class="subtitle">把每门课的学习状态留下记录，便于复习和调整。</p></div><img class="logo" src="{logo}" alt=""></div>
    <div class="ai-wrap"><div><div class="checklist">{tracking}</div><div class="notice">启动后需要学生提供：{esc(materials)}。</div></div><div><img class="ip-mid" src="{ip_exam}" alt=""><img class="ip-mid" src="{ip_grad}" alt=""></div></div>
    <div class="footer"><span>AI LEARNING SPACE</span><span>07</span></div>
  </section>
</main>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_html")
    args = parser.parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid client support proposal intake: " + "; ".join(errors))
    output = Path(args.output_html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(data, skill_dir), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
