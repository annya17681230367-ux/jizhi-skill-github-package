---
name: dp-proposal-designer
description: Create client-facing DP/安心包/卓越安心包 academic support proposals for university students using course information, official programme/module research, risk assessment, workload estimates, service scope, execution rhythm, team configuration, quality-control promises, optional quote pages, and WeChat follow-up copy. Use when the user asks to 做DP方案, DP安心包, 卓越安心包, 保分方案, 65+方案, Distinction方案, 学年包升级DP, 全年/三学期/单学期托管方案, client-facing proposal PDF/HTML, or when they provide school/program/course selections and want a polished academic service plan.
---

# DP Proposal Designer

## Purpose
Generate polished DP academic proposal packages that help sales explain why a student needs managed, long-cycle support rather than one-off assignment help.

Default language: Chinese. Default client deliverable: HTML visual proposal plus PDF export when the local environment supports it.

## Default Workflow

1. Normalize the intake:
   - School, programme, degree level, year/term, target score, product name.
   - Course list by term with credits/UOC/CATS, required/elective/capstone labels, and known assessment details.
   - Student baseline: current grades, weak points, failed/near-failed modules, exam anxiety, writing/language ability, budget sensitivity.

2. Research official course information when course codes or programme names are provided:
   - Use official university programme pages, handbook/module catalogue/course outline pages, timetable pages, and official PDFs first.
   - Capture official course aims, credits, teaching term, assessment components, word counts, exam/presentation/project weights, and prerequisites where available.
   - If assessment weights are not publicly accessible, state that the latest Moodle/Blackboard/Course Outline/brief must confirm them. Do not present inferred weights as official.

3. Diagnose risk:
   - Score by target pressure, assessment difficulty, workload volume, timeline concentration, student baseline, and materials completeness.
   - Translate risk into constructive client-facing language: `需要重点把控`, `建议提前建档`, `适合用DP做节点管理`.

4. Choose the DP product:
   - `DP安心包`: use for pass/60+/65+ stability, weak foundation, exam pressure, prior fail/soft fail, or multi-course management.
   - `DP卓越安心包`: use for Distinction/70+/high Merit, dissertation/capstone-heavy scope, high-value customers, postgraduate application goals, or low tolerance for quality variance.
   - `毕业无忧`: use for final-year/graduation-stage coursework, dissertation, capstone, or degree-classification pressure.

5. Build the proposal:
   - Include the official course structure, workload estimates, target-score strategy, why DP is needed, service contents, team configuration, process flow, course-by-course service plan, next materials needed, and optional quote page.
   - Separate client-facing content from internal notes. Do not expose internal pricing formulas, margin, bottom line, or negotiation room.

6. Export and verify:
   - Prefer single-file HTML as editable source, then export to PDF with browser print.
   - Check that the PDF is valid, not blank, readable in Chinese, and has no internal memo unless explicitly requested.

## Proposal Structure

Use `references/dp_proposal_patterns.md` for detailed module patterns. Default section order:
If the user asks for fixed templates, case templates, 纯DP固定模板, DP模板, or reproducible GitHub/shared-user outputs, read `references/fixed_dp_template_cases.md` before drafting and follow that module order.

1. Cover: school + programme + year/term + target + product. Do not show internal/publication labels such as `客户发送版`, `样例模板`, `官网检索版`, or `报价确认版` on the client cover unless the user explicitly asks.
2. Client situation and proposal conclusion.
3. Official course structure and assessment table.
4. Workload estimate or course-by-course difficulty map.
5. Target-score management logic: 60+/65+/Distinction.
6. Why DP is required.
7. DP service contents and minimum service safeguards.
8. Team configuration and responsibility split.
9. Macro service process and single-assignment process.
10. Quote status or quote page, only when requested. If the user asks for DP报价, read `references/dp_pricing_rules.md` and continue with an internal quote draft even when final prices require核对.
11. Official sources and materials still needed.

## Client-Safe Language

Do not write:
- `保证高分`, `保过`, `100%无风险`, `学校查不到`, `代考`, `无需客户配合`.
- Absolute score guarantees in client-facing text.
- Internal formulas,底价,利润,折扣空间, or unapproved refund/赔付 claims.

Prefer:
- `围绕65+目标做风险管理`.
- `按评分标准进行结构、证据、引用和表达把控`.
- `通过课程建档和节点管理降低返工风险`.
- `保障以合同条款和客户配合事项为准`.
- `以最新 Moodle / brief / rubric 为最终依据`.

## Output Defaults

For unspecified format, produce:
- Client-facing HTML proposal.
- PDF export.
- Short WeChat sending copy.
- Internal memo only if risk/pricing/sales strategy matters, and keep it outside the client PDF.

If the user asks for DP价格、报价、报价单、费用、总价、原价、折后价、内部报价 or 客户报价:

- Read `references/dp_pricing_rules.md`.
- Do not use 学业规划陪跑 pricing formulas.
- Do not stop only because final price files are missing; create a reviewable internal quote draft with `待价格文件核对` where needed.
- Show included DP tasks and excluded exam/test/quiz/tutoring tasks clearly.
- Only block when the user demands a final client-facing amount and no price file, target price, or approved pricing rule exists.

For filenames, when the user gives a naming rule, follow it exactly. Common DP filename format:
`学校_专业_学期_产品.pdf`, for example `UNSW_MComAccounting_T3_DP安心包.pdf`.

## Brand Visual Defaults

Use the Distinction Pass / 极致教育 brand assets when creating client-facing DP方案 unless the user asks for another style:

- Primary logo: `assets/distinction-pass-logo-wide.png`.
- Small icon: `assets/distinction-pass-icon.png`.
- Primary palette from the provided VI source: brand blue `#005CFF`, DiDi Mint `#3BDBBD`, light cyan `#65C8D0`, soft periwinkle `#838BC5`, soft violet `#BA9BC9`, neutral grey `#666666`, white backgrounds.
- Preferred proposal style: clean consulting layout, white/brand-blue/cyan hero, dense course/assessment tables, process cards, timeline, and subtle brand texture accents. Avoid overly dark teal full-page covers unless the user asks for a dark version.
- Use brand reference images only as visual guidance; do not place large VI reference sheets in final proposals unless the user explicitly asks.

## Bundled Reference

- `references/dp_proposal_patterns.md`: design patterns learned from existing DP proposal examples, including module blocks, course tables, target-score framing, DP service claims, quote handling, and quality checks.
- `references/brand_visual_guidelines.md`: logo, palette, VI/IP asset usage, and DP proposal visual defaults.
- `references/dp_pricing_rules.md`: DP-only quote workflow, required fields, scope classification, quote boundaries, and must-continue behavior when prices need核对.
- `references/fixed_dp_template_cases.md`: confirmed pure-DP proposal and DP assessment Excel template rules.

## Bundled Fixed Templates
Use `templates/fixed_cases/` when the user asks for a stable DP output matching the confirmed cases:
- `固定模板06_纯DP服务方案设计.pdf`
- `悉尼大学政治学大三S2_DP全包作业_Assessment整理.xlsx`
- `悉尼大学政治本科三门课考核内容总表.xlsx`
