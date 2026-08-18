---
name: jizhi-academic-year-plan-proposal
description: 极致学业规划年度方案生成。Use when the user wants to generate, revise, or template-match a client-facing annual academic planning proposal, 全年课业规划方案, 学业管家方案, 学业规划方案, AI智慧学习系统方案, course-by-course year plan, term plan, hour allocation plan, quote sheet, branded HTML/PDF proposal, or a proposal following the neon-hamster Netlify template. Trigger when inputs include school, major/program, year, courses/modules, term dates, DDLs, target grade, service hours, AI智慧学习系统, 专业课/陪跑课/规划执行课, 极致AI logo/IP形象, or requests like “按这个模板出方案/做成skill/生成年度方案”. If a request mentions DP安心包, 卓越安心包, Distinction Pass, 65+方案, 保分方案, or DP方案, route by `references/scenario_routing.md` so DP方案 and 学业规划陪跑方案 stay separate.
---

# 极致学业规划年度方案

## Purpose
Generate a client-facing annual academic planning proposal modeled on the referenced Netlify page: a dense but readable consulting-style page that explains why the plan is configured this way, how each course is handled, how hours are allocated, how the year is staged, and how the AI智慧学习系统 plus human teachers create an execution loop.

Default language: Chinese.

Default positioning: use `学业规划`, `学业管家`, `年度课业规划`, `规划执行课`, and `AI智慧学习系统`. Use `陪跑/陪跑课/陪跑方案` only when the user explicitly asks to keep that wording or the source business package requires it.

## Output Modes
- **First draft is text-first by default.** Unless the user explicitly says `直接出PDF`, `最终版`, `不用确认`, or `直接设计渲染`, the first response should be a structured Markdown/text proposal draft, not HTML/PDF. This draft must make the content and quote logic reviewable before design work.
- **Confirmed proposal becomes HTML/PDF.** After the user confirms the content, create a polished HTML source and render/export a PDF with visual verification.
- **Final proposal and quote sheet are separate by default.** The client proposal must not mention any price, quote, discount, payment, amount, or promotion unless the user explicitly asks to merge quote into the proposal.
- **Quote sheet** is a separate deliverable generated only after the方案 has been confirmed or when the user explicitly asks for a quote based on an existing confirmed方案.
- **HTML proposal** is the editable source artifact and should be delivered as a secondary link when created.
- **WeChat summary**: include when sales needs quick forwarding copy.
- **Internal notes**: include when assumptions, missing information, risk, or quote logic need separation from client-facing text.

If the user says “按这个模板”, use `references/template_spec.md` first.
If the user asks for visual style or web page output, use `references/html_style_spec.md`.
If the proposal includes AI智慧学习系统, course classification, or weekly service execution, use `references/service_logic.md`.
If the output is a branded HTML/PDF proposal or quote sheet, use `references/brand_visual_spec.md` and the bundled `assets/` files.
If the user asks for a quote sheet, price, 报价, 报价单, 原价, 折后价, or package comparison, use `references/pricing_quote_rules.md` and read the two required pricing materials before calculating.
If the user asks for 对公版, 精简版, 纯课程考核+报价版, 内部报价版, or 客户报价版, use the version rules in this SKILL.md and keep proposal/quote boundaries clear.
If the request may be DP/安心包/卓越安心包/Distinction Pass/65+方案, first use `references/scenario_routing.md` to decide whether to route to DP logic or学业规划陪跑 logic. Never mix DP quote logic with陪跑 quote logic.
If the user asks for fixed templates, case templates, 模板案例, 产出一致, or wants GitHub/shared users to reproduce the same output, use `references/fixed_template_cases.md` before drafting and match the selected template family.

## Required Inputs
Do not block on every missing field. Ask only when missing data materially changes course classification, hour allocation, or timeline.

Core:
- 学校、专业/项目、学位层级、年级/学年
- 课程清单，最好含英文 module title/code
- 学期/校历/开学日期/考试或DDL节点
- 学生基础、目标分数、薄弱点、当前担心
- 服务范围：全年、单学期、暑期预习、单课程组合
- 服务模式：标准套餐 or 定制方案. If not stated, default to标准套餐.
- 课时或预算：总课时、专业课、规划执行课/陪跑课、AI智慧学习系统是否包含. If not explicitly specified, do not invent定制课时; use标准套餐规则.

If course details are missing, produce a `待补充资料清单` and mark course-level details as `暂估`.

## Official Course Evidence Rule
- Course facts must come from official school sources whenever possible: university handbook, programme page, module catalogue, unit outline, official timetable, or official PDF.
- For every course in the first draft, include source links or file/source names.
- Every first draft must include concrete assessment details when available: assessment name, weight, type, DDL/week, word count/page count/duration, group/individual, exam/test/presentation/writing flags, and source.
- Do not convert unsupported assumptions into facts. If the official page does not publish the detail, write `待Canvas/Moodle/Assessment Brief/Rubric确认`.
- Do not write invented workload estimates as official workload. If a workload judgment is needed without official word count/duration, label it as execution planning advice, not official assessment data.

## Version Modes
Use these modes when requested:
- `标准客户版`: complete client proposal, branded, no quote inside.
- `对公版`: restrained wording, no or weak logo if requested, concise commercial language, proposal and quote still separate unless explicitly merged.
- `精简版`: 1-2 pages after confirmation; keep only diagnosis, course assessment, service match, timeline, and expected effect.
- `纯课程考核+报价版`: if explicitly requested, focus on official assessment, service match, and separate quote sheet; do not include full annual narrative.
- `内部报价版`: may show calculation logic, file references, assumptions, and review flags; not client-facing.
- `客户报价版`: show service items, course workload, original price, discounts, final price, and boundary notes; do not expose internal margin, bottom line, or negotiation room.

## Service Value Logic
Every proposal, including text-first drafts, must show what the client receives and why it matters. Cover the six planning logic items:
- 个人学业画像.
- 问题诊断与定位.
- 目标差距分析.
- 课程优先级.
- 阶段行动建议.
- 学业风险清单.

Also include:
- 服务内容: what the team does for the student and parent.
- 服务价值: why this reduces risk or improves execution.
- 预期效果: what should improve by each stage, without guaranteed grade/pass claims.

## Workflow
0. Scenario route:
   - If the user asks for DP安心包, 卓越安心包, Distinction Pass, 65+/60+目标管理, 保分方案, 学年包升级DP, or “DP方案”, follow `references/scenario_routing.md` and use DP proposal logic/pricing boundaries.
   - If the user asks for 学业规划, 全年陪跑, 课业陪跑, 学业管家, AI智慧学习系统, 标准套餐/定制陪跑, use this skill’s学业规划陪跑 workflow.
   - If the request contains both, ask or clearly split deliverables into `DP方案` and `学业规划陪跑方案`; do not combine their quote formulas.
1. Decide output stage:
   - If this is a first draft, produce a structured Markdown/text proposal. Do not render HTML/PDF.
   - If the user confirms the draft or asks for final/design/PDF, generate HTML/PDF and visually verify.
2. Normalize intake into a structured brief.
3. Research and cite official course evidence. If official details are unavailable, mark pending materials clearly.
4. Build the core judgment: explain the student’s real risk, not just the course list.
5. Generate the first-draft assessment table:
   - course code/title
   - official assessment components, weights, DDL/week, word count/duration
   - group/exam/writing/presentation flags
   - official source or `待确认`
   - workload and start-time judgment, clearly separated from official facts
6. Classify courses by cluster and priority:
   - cluster examples: Industry, Management, Professional Practice, Technology, Writing, Quantitative, Research, Studio.
   - priority: 重点 / 非重点, plus risk level 低/中/中高/高.
7. Allocate hours:
   - Default first rule: unless the user explicitly says `定制方案`, `定制课时`, `按具体逻辑算`, or gives exact per-course hours, use标准套餐. Only use course content, assessment risk, student ability, and DDL density to classify each course as重点 or 非重点.
   - 标准套餐 hours come from the current questionnaire/pricing material: 重点课程 = 6节专业课 + 10节规划执行/陪跑课; 非重点课程 = 2节专业课 + 8节规划执行/陪跑课, unless the current questionnaire says otherwise.
   - Use the user’s exact custom numbers only when定制方案 is explicitly requested.
   - Show total hours and split between specialist teaching and planning/execution support.
   - If numbers are estimated or pending official assessment data, label them clearly as `暂估`.
8. Generate course cards for each module:
   - 中文课程名
   - English module title/code
   - Assessment focus
   - Risk judgment
   - Service strategy
   - Hour split and total
9. Generate term/stage arrangement using real dates when available.
10. Generate the concrete annual path:
   - 诊断 -> 建档 -> 开学资料抓取 -> 每周执行 -> 作业节点 -> 考试/口试冲刺 -> 出分复盘.
11. Generate weekly loop:
   - 资料同步 -> 专业课深讲 -> AI智慧学习系统练习检测 -> 规划执行课复盘 -> 周报与下周计划.
12. Generate AI智慧学习系统 usage path and course-specific learning-system usage.
13. Generate service delivery modules, service value, expected effect, and resource configuration.
14. Add assumptions, material request list, and quality check.
15. Do not generate the quote sheet until the proposal is confirmed or a separate quote instruction is issued.
16. Final confirmed proposal: export to PDF and visually verify the PDF before delivery; keep quote as a separate file unless explicitly merged.

## Proposal Structure
For text-first drafts, use a compact Markdown version of this structure. For confirmed HTML/PDF proposals, follow this order unless the user asks for a shorter version:
1. Header: brand, school/program/year label, proposal title, one-paragraph positioning.
2. KPI cards: total hours, specialist hours, planning/execution hours, number of courses.
3. 核心判断: why this student needs the plan; include hour ratio visualization.
4. 课程分类:重点/非重点 and allocation principles.
5. 学生背景诊断: 3 cards for program fit, ability risk, service strategy.
6. 课程分类与课时配置: one card per course.
7. 校历阶段安排: phase table with dates, weeks, hours, focus.
8. 全年具体路径: horizontal steps with time range, action, output.
9. 每周执行闭环: 5-step weekly operating model.
10. DDL与Assessment节点: official assessment components, DDL/week, word count/duration, concrete timeline, and student cooperation requirements.
11. AI智慧学习系统使用路径.
12. AI智慧学习系统在各课程中的具体用法.
13. 服务交付模块.
14. AI与老师资源配置.
15. 服务价值与预期效果.
16. Footer: source/assumption note and “正式执行以学生入学后 Handbook/Moodle/Assessment Brief 为准”.

## Quote Sheet Structure
Quote sheets are separate from the proposal unless explicitly merged. A quote sheet must include:
- Quote version: internal or client-facing.
- Source proposal/version/date.
- Per-course service content and workload basis.
- Service mode: 标准套餐 / 门数折扣 / 定制方案 / 混合方案.
- Course classification and hours.
- Original price.
- Discount logic from pricing files, including course-count/package discount when applicable.
- Final discounted price.
- Add-ons included or excluded.
- Pricing source files and two-pass arithmetic check.

## Client-Facing Language Rules
- Sound like a professional education consulting proposal, not an ad slogan.
- Explain tradeoffs: why some courses are high-risk, why hours are split that way, why the AI智慧学习系统 is used.
- Avoid guaranteed outcomes: do not say 保分、保过、保证高分.
- Replace negative blame with risk-control language:
  - “需要重点把控”
  - “建议提前建档”
  - “正式执行后根据Moodle/Brief动态调整”
- Make parent value visible: they see progress, risk, next action, and feedback, not just class count.

## Bundled References
- `references/template_spec.md`: exact module order and content requirements from the template.
- `references/fixed_template_cases.md`: confirmed fixed case templates, output routing, module order, and consistency rules.
- `references/service_logic.md`: course classification, hour allocation, AI智慧学习系统 and weekly loop logic.
- `references/html_style_spec.md`: single-page HTML visual style matching the template.
- `references/brand_visual_spec.md`: 极致AI logo/IP visual rules, page header requirements, color tokens, and image placement.
- `references/scenario_routing.md`: DP方案 vs 学业规划陪跑方案 scenario detection and hard separation of proposal/quote logic.
- `references/pricing_quote_rules.md`: quote boundary, standard-package vs custom pricing rules, required pricing materials, original/discounted price fields, and pre-export quote verification.
- `references/quality_check.md`: final checklist and scoring.
- `references/example_prompt.md`: sample request that should trigger this skill.

## Bundled Assets
Use bundled assets by absolute path from this skill folder when generating HTML/PDF:
- `assets/brand/full-logo.jpg`: required full horizontal logo for the upper-left page/header area.
- `assets/ip/study-dashboard.jpg`: AI learning system, planning, dashboard, or service flow pages.
- `assets/ip/research-files.jpg`: material collection, course pack, diagnosis, or document research pages.
- `assets/ip/report-scroll.jpg`: report, pathway, final delivery, or action plan pages.
- `assets/ip/portrait-star.jpg` and `assets/ip/standing.jpg`: light page fillers in empty side space.
- `assets/ip/graduation.jpg`, `assets/ip/cheer.jpg`, `assets/ip/pass-test.jpg`, `assets/ip/checklist.jpg`: outcome, milestone, assessment, and risk-control scenes.

## Bundled Fixed Templates
Use `templates/fixed_cases/` as the authoritative fixed-output examples when the user asks for a stable/reproducible template:
- 标准年度学业规划方案.
- 对公精简服务匹配方案.
- 独立报价单.
- Excel课程考核与报价整理表.
- DP加陪跑混合边界方案.
- 纯DP服务方案设计.
- Confirmed skill case and template description document.
