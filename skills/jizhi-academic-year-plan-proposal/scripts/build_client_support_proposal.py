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
    quote = data.get("quote")
    if quote:
        for key in ("planning_total", "dp_total", "combined_total"):
            if not quote.get(key):
                errors.append(f"quote missing {key}")
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


def dp_item(item):
    pending = item.get("pending")
    pending_html = f"<small>待确认：{esc(pending)}</small>" if pending else ""
    return f"""
    <div class="dp-item">
      <b>{esc(item.get('course'))}</b>
      <span>{esc(item.get('assessment'))} · {esc(item.get('scope'))}</span>
      <p>{esc(item.get('support'))}</p>
      {pending_html}
    </div>
    """


def money_stat(value, label, note=""):
    return f"<div class='money'><b>{esc(value)}</b><span>{esc(label)}</span><small>{esc(note)}</small></div>"


def quote_line(item):
    return f"""
    <tr>
      <td>{esc(item.get('item'))}</td>
      <td>{esc(item.get('scope'))}</td>
      <td>{esc(item.get('amount'))}</td>
    </tr>
    """


def build_sim_html(data, skill_dir):
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
    dp_modules = data.get("dp_modules", [])
    dp_module_html = "".join(dp_item(x) for x in dp_modules)
    dp_section = ""
    if dp_modules:
        dp_section = f"""
        <div class="dp-panel">
          <h3>DP 作业保障范围</h3>
          <p>DP 只覆盖已列出的作业/论文/项目类考核；线下考试、在线测验、出勤和课堂学习仍由专业课与陪跑节奏承接。</p>
          <div class="dp-grid">{dp_module_html}</div>
        </div>
        """
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
.dp-panel {{ margin-top:7mm; background:#fff; border:1px solid var(--line); border-radius:8px; padding:6mm; }}
.dp-panel h3 {{ margin:0 0 2mm; font-size:15px; color:var(--ink); }}
.dp-panel > p {{ margin:0 0 4mm; color:#526a8b; font-size:11px; line-height:1.65; }}
.dp-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:4mm; }}
.dp-item {{ border-left:4px solid var(--cyan); background:#f7fbff; padding:4mm; border-radius:6px; min-height:27mm; }}
.dp-item b,.dp-item span,.dp-item small {{ display:block; }}
.dp-item b {{ color:var(--ink); font-size:12px; margin-bottom:1mm; }}
.dp-item span {{ color:var(--blue); font-size:10px; font-weight:800; margin-bottom:1mm; }}
.dp-item p {{ margin:0; color:#526a8b; font-size:10px; line-height:1.45; }}
.dp-item small {{ color:#8a6a00; font-size:9px; margin-top:1mm; }}
.quote-page {{ background:linear-gradient(135deg,#f6faff 0%,#edf6ff 72%,#e4fffb 100%); }}
.quote-band {{ background:var(--blue); color:#fff; margin:-18mm -18mm 10mm -18mm; padding:15mm 18mm 18mm; position:relative; overflow:hidden; }}
.quote-band:after {{ content:""; position:absolute; right:-24mm; bottom:-30mm; width:78mm; height:78mm; border-radius:50%; background:var(--cyan); }}
.quote-band h1 {{ color:#fff; font-size:31px; margin:7mm 0 0; position:relative; z-index:1; }}
.quote-stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6mm; margin-bottom:7mm; }}
.money {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:8mm; }}
.money b {{ display:block; color:var(--blue); font-family:Montserrat,"Avenir Next",Arial,sans-serif; font-size:27px; }}
.money span,.money small {{ display:block; color:#4b6385; font-size:11px; line-height:1.5; }}
.quote-table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:8px; overflow:hidden; font-size:12px; }}
.quote-table th {{ background:#eaf4ff; color:#123c75; text-align:left; padding:10px; }}
.quote-table td {{ border-top:1px solid var(--line); padding:10px; color:#445f82; line-height:1.45; }}
.quote-note {{ margin-top:7mm; background:#fff8df; border:1px solid #ffe28c; border-radius:8px; padding:6mm; color:#6b581a; font-size:11px; line-height:1.7; }}
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
    <div class="ai-wrap"><div><div class="checklist">{tracking}</div>{dp_section}<div class="notice">启动后需要学生提供：{esc(materials)}。</div></div><div><img class="ip-mid" src="{ip_exam}" alt=""><img class="ip-mid" src="{ip_grad}" alt=""></div></div>
    <div class="footer"><span>AI LEARNING SPACE</span><span>07</span></div>
  </section>
</main>
</body>
</html>"""


def course_row(course):
    lessons = f"专业课 {course.get('professional_lessons')} 节 + 陪跑课 {course.get('pacing_lessons')} 节"
    return f"""
    <tr>
      <td>{esc(course.get('name'))}<br><small>{esc(course.get('cn'))}</small></td>
      <td>{esc(course.get('assessment') or course.get('watch'))}</td>
      <td>{esc(course.get('service_path') or lessons)}</td>
      <td>{esc(course.get('support'))}</td>
    </tr>
    """


def role_row(role):
    return f"<tr><td>{esc(role.get('title'))}</td><td>{esc(role.get('text'))}</td></tr>"


def ucl_stat(value, label, note=""):
    return f"<div class='stat'><b>{esc(value)}</b><span>{esc(label)}</span><p>{esc(note)}</p></div>"


def workflow_card(index, title, text):
    return f"<div class='workflow-card'><b>{index:02d} {esc(title)}</b><p>{esc(text)}</p></div>"


def build_html(data, skill_dir):
    if data.get("visual_style") == "sim_dit":
        return build_sim_html(data, skill_dir)

    assets = skill_dir / "assets"
    logo = asset_uri(assets / "brand/full-logo.jpg")
    ip_cover = asset_uri(assets / "ip/cheer.jpg")
    ip_grad = asset_uri(assets / "ip/graduation.jpg")

    student = data["student"]
    targets = data["targets"]
    lesson = data["lesson_plan"]
    professional = int(lesson["professional_lessons"])
    pacing = int(lesson["pacing_lessons"])
    total = int(lesson["total_lessons"])
    courses = data["courses"]
    dp_modules = data.get("dp_modules", [])
    has_dp = bool(dp_modules)
    materials = "、".join(data.get("materials_needed", []))
    boundary = data.get("boundary_note") or "正式执行以学校handbook、课程平台、Assessment Brief、个人课表和考试安排为准。"

    profile = student.get("profile", [])
    diagnosis_cards = "".join(
        f"<div class='box'><h3>{esc(item.get('label'))}</h3><p><b>{esc(item.get('value'))}</b><br>{esc(item.get('note'))}</p></div>"
        for item in profile[:2]
    )
    if not diagnosis_cards:
        diagnosis_cards = (
            f"<div class='box'><h3>当前基础</h3><p>{esc(student.get('school'))} {esc(student.get('program'))}，{len(courses)} 门课程进入全年建档。</p></div>"
            f"<div class='box warn'><h3>年度风险</h3><p>考试、作业、出勤和DDL节点需要统一管理，避免临时启动。</p></div>"
        )

    tiers = lesson.get("tiers", [])
    tier_cards = "".join(ucl_stat(t.get("value"), t.get("label"), t.get("note")) for t in tiers[:4])
    if not tier_cards:
        tier_cards = (
            ucl_stat(str(len(courses)), "课程数量", "按课程风险和考核形式配置服务。")
            + ucl_stat(str(professional), "专业课", "优先解决课程理解、题型和考前输出。")
            + ucl_stat(str(pacing), "陪跑课", "用于建档、周任务、DDL和阶段复盘。")
        )

    course_table = "".join(course_row(c) for c in courses)
    role_table = "".join(role_row(r) for r in data["roles"])
    roadmap = "".join(
        f"<div class='phase'><b>{esc(item.get('label'))}</b><p><strong>{esc(item.get('title'))}</strong><br>{esc(item.get('text'))}</p><small>{esc(item.get('owner'))}</small></div>"
        for item in data["roadmap"]
    )
    tracking = "".join(f"<div class='track'><h3>{esc(x.get('title'))}</h3><p>{esc(x.get('text'))}</p></div>" for x in data["tracking"][:4])

    dp_rows = "".join(
        f"<tr><td>{esc(x.get('course'))}</td><td>{esc(x.get('assessment'))}</td><td>{esc(x.get('scope'))}</td><td>{esc(x.get('support'))}</td></tr>"
        for x in dp_modules
    )
    dp_page = ""
    if has_dp:
        dp_page = f"""
  <section class="page">
    <div class="kicker">03 · DP WORKLOAD</div><h2>DP作业保障范围</h2>
    <table><thead><tr><th>课程</th><th>主要考核</th><th>服务深度</th><th>DP管理内容</th></tr></thead><tbody>{dp_rows}</tbody></table>
    <div class="notice">DP只覆盖已列明的作业/论文/项目类考核；线下考试、在线测验、出勤和课堂学习仍由专业课与陪跑节奏承接。</div>
    <h2 class="subhead">DP单项执行路径</h2>
    <div class="workflow">
      {workflow_card(1, "资料建档", "Brief、Rubric、DDL、导师反馈和reading统一归档。")}
      {workflow_card(2, "任务卡", "明确评分点、结构、材料、版本节点和风险。")}
      {workflow_card(3, "方向与结构", "先确认论点与评分标准对应，再进入内容推进。")}
      {workflow_card(4, "阶段版本", "大纲、初稿、70%版本、质检版本可追踪。")}
      {workflow_card(5, "多层质检", "结构、证据、引用、语言、格式及原创风险检查。")}
      {workflow_card(6, "反馈迭代", "结合导师反馈与成绩调整下一项任务策略。")}
    </div>
    <div class="footer"><span>DP项目工作量与执行流程</span><span>04</span></div>
  </section>
        """

    support_title = "考试/专业课支持" if has_dp else "课时结构与阶段安排"
    support_rows = "".join(
        f"<tr><td>{esc(c.get('name'))}</td><td>{esc(c.get('professional_lessons'))} 节</td><td>{esc(c.get('pacing_lessons'))} 节</td><td>{esc(c.get('support'))}</td></tr>"
        for c in courses
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{esc(student.get('program'))} 学业规划方案</title>
<style>
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#fff; color:#061b43; font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif; letter-spacing:0; }}
.page {{ width:210mm; height:297mm; margin:0 auto; position:relative; overflow:hidden; background:#fff; padding:19mm 16mm 14mm; page-break-after:always; }}
.page:last-child {{ page-break-after:auto; }}
.page:before {{ content:""; position:absolute; top:0; left:0; right:0; height:5mm; background:linear-gradient(90deg,#0062ff,#17dbc8,#9aa7c4); }}
.logo {{ width:45mm; height:auto; object-fit:contain; }}
.kicker {{ font-size:12px; letter-spacing:3px; color:#0062ff; font-weight:900; text-transform:uppercase; }}
h1,h2 {{ margin:0; color:#0a3271; font-weight:850; letter-spacing:0; }}
h1 {{ font-size:34px; line-height:1.18; }}
h2 {{ font-size:30px; line-height:1.2; margin-top:8mm; }}
.subhead {{ font-size:26px; margin-top:12mm; }}
h3 {{ margin:0 0 5px; font-size:16px; color:#0054d9; }}
p,li {{ font-size:13px; line-height:1.65; color:#183359; }}
.footer {{ position:absolute; left:16mm; right:16mm; bottom:9mm; border-top:1px solid #d6e5f7; padding-top:4mm; display:flex; justify-content:space-between; color:#7b8aa6; font-size:10px; }}
.cover {{ padding-top:22mm; }}
.hero {{ margin-top:26mm; border-radius:24px; background:linear-gradient(135deg,#113b8f 0%,#0062ff 55%,#22d6ca 100%); color:#fff; padding:18mm 14mm; min-height:92mm; }}
.hero .kicker,.hero h1,.hero p {{ color:#fff; }}
.hero p {{ font-size:16px; max-width:150mm; }}
.chips {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:10mm; }}
.chip {{ border:1px solid rgba(255,255,255,.6); border-radius:999px; padding:7px 13px; font-size:12px; color:#fff; }}
.stat-row {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:12mm; }}
.stat {{ border:1px solid #c9dcf4; border-radius:12px; background:#f8fbff; padding:16px; min-height:34mm; }}
.stat b {{ display:block; font-size:32px; color:#0062ff; }}
.stat span {{ font-weight:800; color:#0054d9; }}
.stat p {{ margin:5px 0 0; font-size:12px; }}
.judgment {{ border-left:4px solid #20d6c6; margin-top:10mm; padding-left:8mm; color:#0a3271; font-size:18px; line-height:1.5; font-weight:700; }}
.ip {{ position:absolute; right:18mm; bottom:25mm; width:45mm; height:45mm; object-fit:contain; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:10mm; }}
.box {{ border:1px solid #c9dcf4; border-radius:12px; background:#f8fbff; padding:14px; min-height:43mm; }}
.box.warn,.notice {{ background:#fff7e5; border-color:#ffc640; }}
.box.green {{ background:#edfffb; border-color:#3bd9c8; }}
.box ul {{ margin:5px 0 0; padding-left:18px; }}
.target-row {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:13mm; }}
.target {{ border:1px solid #c9dcf4; border-radius:12px; padding:16px; background:#f8fbff; }}
.target.green {{ background:#effffc; border-color:#3bd9c8; }}
.target b {{ display:block; font-size:29px; color:#0062ff; }}
.target span {{ font-weight:850; color:#0054d9; }}
.steps {{ margin-top:12mm; display:grid; gap:13px; }}
.step {{ display:grid; grid-template-columns:22mm 1fr; gap:12px; align-items:start; }}
.dot {{ width:13mm; height:13mm; border-radius:50%; background:#0062ff; border:4px solid #d8fff8; box-shadow:0 0 0 2px #31ddca; }}
.step h3 {{ margin-top:0; }}
.step p {{ margin:0; }}
table {{ width:100%; border-collapse:collapse; margin-top:10mm; font-size:11.2px; border:1px solid #c9dcf4; }}
th {{ background:#0d438d; color:#fff; text-align:left; padding:9px; font-weight:850; }}
td {{ padding:8px; border-top:1px solid #c9dcf4; vertical-align:top; color:#10294e; line-height:1.42; }}
td small {{ color:#51698a; }}
tbody tr:nth-child(even) td {{ background:#f3f8ff; }}
.mini-panel {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:10mm; }}
.mini {{ border:1px solid #c9dcf4; border-radius:12px; background:#f8fbff; padding:15px; }}
.mini.green {{ background:#edfffb; border-color:#3bd9c8; }}
.mini p {{ margin:0; }}
.workflow {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:12mm; }}
.workflow-card {{ border:1px solid #c9dcf4; border-radius:12px; background:#f8fbff; padding:14px; min-height:35mm; }}
.workflow-card b {{ display:block; color:#0062ff; font-size:19px; margin-bottom:5px; }}
.workflow-card p {{ margin:0; font-size:12px; }}
.big-metrics {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:12mm 0; }}
.big {{ border:1px solid #c9dcf4; border-radius:12px; background:#f8fbff; padding:18px; }}
.big b {{ display:block; font-size:34px; color:#0062ff; }}
.big p {{ margin:4px 0 0; }}
.phase {{ display:grid; grid-template-columns:28mm 1fr 32mm; gap:10px; align-items:start; border-bottom:1px solid #e1ecfa; padding:8px 0; }}
.phase b {{ color:#0062ff; font-size:16px; }}
.phase p {{ margin:0; }}
.phase small {{ color:#008f83; font-weight:800; }}
.track-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:13mm 0; }}
.track {{ background:#f8fbff; border:1px solid #c9dcf4; border-top:5px solid #0062ff; border-radius:8px; padding:13px; min-height:42mm; }}
.track p {{ margin:0; font-size:12px; }}
.notice {{ margin-top:9mm; border:1px solid #ffc640; border-radius:12px; padding:15px; color:#6b5300; font-size:13px; line-height:1.6; }}
</style>
</head>
<body>
<main>
  <section class="page cover">
    <img class="logo" src="{logo}" alt="">
    <div class="hero">
      <div class="kicker">{esc(student.get('headline') or 'ACADEMIC SUPPORT PLAN')}</div>
      <h1>{'全年DP安心包<br>与考试陪跑方案' if has_dp else '全年学业规划<br>与课程陪跑方案'}</h1>
      <p>面向 {esc(student.get('entry_date'))} 的 {esc(student.get('program'))}，围绕课程考核、专业学习、阶段节点和过程沉淀配置全年支持。</p>
      <div class="chips"><span class="chip">{esc(student.get('school'))}</span><span class="chip">{len(courses)} 门课程</span><span class="chip">专业课 {professional} 节</span><span class="chip">陪跑课 {pacing} 节</span></div>
    </div>
    <div class="stat-row">
      {ucl_stat(targets.get('baseline'), '底线目标', '先降低漏交、失控复习和考试失误风险。')}
      {ucl_stat(targets.get('main'), '主目标', '围绕核心课程和可拉分任务推进。')}
      {ucl_stat(str(total) + 'h', '常规授课', f'专业课 {professional}h + 陪跑课 {pacing}h。')}
    </div>
    <div class="judgment">这不是单门补课问题，而是多门课程、不同考核模式与多个DDL节点的全年项目制管理问题。</div>
    <img class="ip" src="{ip_cover}" alt="">
    <div class="footer"><span>学业规划｜年度服务方案</span><span>01</span></div>
  </section>

  <section class="page">
    <div class="kicker">01 · STUDENT DIAGNOSIS</div><h2>学情判断与全年目标</h2>
    <div class="grid2">{diagnosis_cards}</div>
    <div class="target-row">
      <div class="target green"><span>底线目标</span><b>{esc(targets.get('baseline'))}</b><p>以课程过程稳定和关键考核不失控为前提。</p></div>
      <div class="target"><span>主目标</span><b>{esc(targets.get('main'))}</b><p>按课程风险分层推进专业课、陪跑和DP任务。</p></div>
      <div class="target"><span>冲刺目标</span><b>{esc(targets.get('stretch'))}</b><p>优势课程争取上探，薄弱课程优先守住底线。</p></div>
    </div>
    <div class="steps">
      <div class="step"><div class="dot"></div><div><h3>先稳住过程</h3><p>所有课程完成建档、权重映射、DDL和考试节点整理，避免漏交与临时启动。</p></div></div>
      <div class="step"><div class="dot"></div><div><h3>再提高输出</h3><p>DP或作业课程抓质量，考试课程抓题型稳定，陪跑只保留必要节点管理。</p></div></div>
      <div class="step"><div class="dot"></div><div><h3>最后形成方法</h3><p>把有效的阅读、计算、答题和复习方法沉淀为后续课程可复用资产。</p></div></div>
    </div>
    <div class="notice">目标边界：本方案为执行目标和风险管理方案，不构成无条件分数承诺；最终成绩受学校评分、考试表现、资料提供及时性和学生配合程度影响。</div>
    <div class="footer"><span>学情诊断与目标策略</span><span>02</span></div>
  </section>

  <section class="page">
    <div class="kicker">02 · COURSE CONFIGURATION</div><h2>{len(courses)}门课程的服务路径配置</h2>
    <table><thead><tr><th>课程</th><th>考核/观察重点</th><th>服务路径</th><th>管理重点</th></tr></thead><tbody>{course_table}</tbody></table>
    <div class="mini-panel"><div class="mini green"><h3>{'DP安心包' if has_dp else '专业课支持'}</h3><p>{'每项DP任务建立任务卡，管理资料、方向、结构、版本、质检和提交核对。' if has_dp else '优先处理课程理解、题型训练、错题复盘和考前输出。'}</p></div><div class="mini"><h3>陪跑执行</h3><p>按课程节点进行资料确认、周任务推进、DDL提醒、出勤/考试节点检查和阶段复盘。</p></div></div>
    <div class="footer"><span>课程考核与服务路径</span><span>03</span></div>
  </section>

  {dp_page}

  <section class="page">
    <div class="kicker">{'04' if has_dp else '03'} · SUPPORT</div><h2>{support_title}</h2>
    <table><thead><tr><th>课程</th><th>专业课</th><th>陪跑课</th><th>核心成果</th></tr></thead><tbody>{support_rows}</tbody></table>
    <div class="big-metrics"><div class="big"><b>{professional}h</b><p>专业课，解决学科内容、题型判断和复杂问题。</p></div><div class="big"><b>{pacing}h</b><p>陪跑课，推进复习、资料、检测、错题和考前节奏。</p></div><div class="big"><b>{total}h</b><p>常规授课合计，专业课占比 {round(professional / total * 100)}%。</p></div></div>
    <div class="mini-panel"><div class="mini green"><h3>阅读与术语</h3><p>保留高频核心术语、公式和概念，要求能解释、能比较、能用于答案。</p></div><div class="mini"><h3>考试输出</h3><p>建立定义-机制-计算/图形-评价结构，从短题逐步过渡到限时套题。</p></div></div>
    <div class="footer"><span>课时与方法</span><span>{'05' if has_dp else '04'}</span></div>
  </section>

  <section class="page">
    <div class="kicker">{'05' if has_dp else '04'} · CALENDAR</div><h2>全年节点推进</h2>
    <div>{roadmap}</div>
    <h2 class="subhead">排课原则</h2>
    <div class="grid2"><div class="box green"><h3>第一优先</h3><p>固定每周学习锚点，避免临近考试或DDL才集中启动。</p></div><div class="box"><h3>可协调时段</h3><p>结合学生Timetable、seminar/tutorial、DDL和考试日期具体排课。</p></div></div>
    <div class="notice">DP不占固定常规授课时段，按作业节点进行资料确认、版本推进和质检；固定排课主要用于专业课和必要陪跑。</div>
    <div class="footer"><span>校历节点与排课策略</span><span>{'06' if has_dp else '05'}</span></div>
  </section>

  <section class="page">
    <div class="kicker">{'06' if has_dp else '05'} · DELIVERY RESPONSIBILITY</div><h2>全年执行责任</h2>
    <table><thead><tr><th>角色</th><th>主要责任</th></tr></thead><tbody>{role_table}</tbody></table>
    <h2 class="subhead">过程沉淀</h2>
    <div class="track-grid">{tracking}</div>
    <div class="notice">启动后需要学生提供：{esc(materials)}。</div>
    <img class="ip" src="{ip_grad}" alt="">
    <div class="footer"><span>服务责任与配合边界</span><span>{'07' if has_dp else '06'}</span></div>
  </section>

  <section class="page">
    <div class="kicker">{'07' if has_dp else '06'} · EXPECTED OUTCOME</div><h2>预期效果与正式执行条件</h2>
    <div class="grid2"><div class="box green"><h3>过程目标</h3><p>课程建档、阶段任务、错题/资料沉淀、考前复习包和关键DDL节点形成可追踪记录。</p></div><div class="box"><h3>成绩目标</h3><p>底线：{esc(targets.get('baseline'))}；主目标：{esc(targets.get('main'))}；冲刺：{esc(targets.get('stretch'))}。</p></div></div>
    <div class="steps"><div class="step"><div class="dot"></div><div><h3>课程资料</h3><p>最新syllabus/course outline、Assessment Brief、Rubric、Reading List和课程平台页面。</p></div></div><div class="step"><div class="dot"></div><div><h3>时间资料</h3><p>个人Timetable、seminar/tutorial、全部DDL、online test时间和考试表。</p></div></div><div class="step"><div class="dot"></div><div><h3>保障确认</h3><p>服务范围、学生配合义务、版本节点和合同保障条款。</p></div></div></div>
    <div class="notice">{esc(boundary)}</div>
    <div class="footer"><span>预期效果与执行条件</span><span>{'08' if has_dp else '07'}</span></div>
  </section>
</main>
</body>
</html>"""


def build_quote_html(data, skill_dir):
    assets = skill_dir / "assets"
    logo = asset_uri(assets / "brand/full-logo.jpg")
    ip_study = asset_uri(assets / "ip/study-dashboard.jpg")
    student = data["student"]
    lesson = data["lesson_plan"]
    quote = data.get("quote") or {}
    professional = int(lesson["professional_lessons"])
    pacing = int(lesson["pacing_lessons"])
    total = int(lesson["total_lessons"])
    rows = "".join(quote_line(x) for x in quote.get("lines", []))
    if not rows:
        rows = (
            quote_line({"item": "专业课 + 陪跑课", "scope": f"专业课 {professional} 节 + 陪跑课 {pacing} 节，共 {total} 节", "amount": quote.get("planning_total")})
            + quote_line({"item": "DP 作业保障", "scope": f"{len(data.get('dp_modules', []))} 个作业/项目考核模块", "amount": quote.get("dp_total")})
        )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{esc(student.get('program'))} 报价单</title>
<style>
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; }}
:root {{ --blue:#005CFF; --cyan:#00EAD3; --ink:#071C3F; --line:#D7E5FF; --muted:#5B6F8F; }}
body {{ margin:0; background:#eaf2ff; color:var(--ink); font-family:"Source Han Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif; letter-spacing:0; }}
.page {{ width:210mm; height:297mm; margin:0 auto; position:relative; overflow:hidden; padding:18mm; }}
.logo {{ width:42mm; height:auto; object-fit:contain; display:block; position:relative; z-index:1; }}
.quote-page {{ background:linear-gradient(135deg,#f6faff 0%,#edf6ff 72%,#e4fffb 100%); }}
.quote-band {{ background:var(--blue); color:#fff; margin:-18mm -18mm 10mm -18mm; padding:15mm 18mm 18mm; position:relative; overflow:hidden; min-height:75mm; }}
.quote-band:before {{ content:""; position:absolute; right:-23mm; bottom:-32mm; width:88mm; height:88mm; border-radius:50%; background:var(--cyan); }}
.quote-band h1 {{ color:#fff; font-size:31px; line-height:1.2; margin:9mm 0 0; position:relative; z-index:1; }}
.quote-band p {{ color:#dceaff; font-size:13px; margin:4mm 0 0; position:relative; z-index:1; }}
.ip {{ position:absolute; right:18mm; top:20mm; width:43mm; height:43mm; object-fit:contain; z-index:1; }}
.quote-stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6mm; margin-bottom:7mm; }}
.money {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:8mm; min-height:38mm; }}
.money b {{ display:block; color:var(--blue); font-family:Montserrat,"Avenir Next",Arial,sans-serif; font-size:27px; }}
.money span,.money small {{ display:block; color:#4b6385; font-size:11px; line-height:1.5; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:8px; overflow:hidden; font-size:12px; }}
th {{ background:#eaf4ff; color:#123c75; text-align:left; padding:10px; }}
td {{ border-top:1px solid var(--line); padding:10px; color:#445f82; line-height:1.45; }}
.note {{ margin-top:7mm; background:#fff8df; border:1px solid #ffe28c; border-radius:8px; padding:6mm; color:#6b581a; font-size:11px; line-height:1.7; }}
.footer {{ position:absolute; left:18mm; right:18mm; bottom:10mm; display:flex; justify-content:space-between; align-items:center; color:#7890b2; font-size:10px; font-family:Montserrat,"Avenir Next",Arial,sans-serif; }}
.footer:before {{ content:""; position:absolute; left:0; right:0; top:-6mm; height:1px; background:#d9e8ff; }}
</style>
</head>
<body>
<section class="page quote-page">
  <div class="quote-band">
    <img class="logo" src="{logo}" alt="">
    <img class="ip" src="{ip_study}" alt="">
    <h1>{esc(student.get('school'))}<br>{esc(student.get('program'))}<br>混合服务报价单</h1>
    <p>专业课 + 轻陪跑 + DP 作业保障分开计价，合计展示。</p>
  </div>
  <div class="quote-stats">
    {money_stat(quote.get('planning_total'), '专业课 + 陪跑课', f'专业课 {professional} 节 / 陪跑课 {pacing} 节')}
    {money_stat(quote.get('dp_total'), 'DP 作业保障', f'{len(data.get("dp_modules", []))} 个作业/项目模块')}
    {money_stat(quote.get('combined_total'), '合计报价', quote.get('validity', '以资料确认后执行为准'))}
  </div>
  <table>
    <thead><tr><th>服务项目</th><th>服务范围</th><th>金额</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <div class="note">{esc(quote.get('pricing_note') or '正式执行前需确认课程表、syllabus、作业 brief、rubric 与 DDL；DP 仅覆盖已列明的作业/项目类考核，不覆盖考试、在线测验、出勤或课堂学习。')}</div>
  <div class="footer"><span>JIZHI AI MIXED SUPPORT QUOTE</span><span>QUOTE</span></div>
</section>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("output_html")
    parser.add_argument("--quote-only", action="store_true", help="render the standalone mixed-service quote page")
    args = parser.parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        raise SystemExit("Invalid client support proposal intake: " + "; ".join(errors))
    output = Path(args.output_html)
    output.parent.mkdir(parents=True, exist_ok=True)
    html_text = build_quote_html(data, skill_dir) if args.quote_only else build_html(data, skill_dir)
    output.write_text(html_text, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
