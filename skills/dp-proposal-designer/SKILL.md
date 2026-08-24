---
name: dp-proposal-designer
description: Generate client-facing pure DP, DP安心包, DP卓越安心包, DP全包作业 and 毕业无忧 proposals, including requests for DP方案并报价; own the proposal and hand final price work to the DP quote skill. Use for DP客户方案, 安心包方案, 全包作业方案, 保分/稳分方案 and DP visual PDF/HTML. Do not use for academic-planning lesson allocation or standalone final-price requests.
---

# DP Proposal Designer

Generate Chinese client-facing DP proposals. This skill owns the DP service proposal and visual presentation, not the final DP price calculation.

## Boundary

- Use for pure DP, 安心包, 卓越安心包, 毕业无忧, coursework/project managed support and the DP portion of a mixed plan.
- Use `jizhi-academic-year-plan-proposal` for planning/陪跑 hours, AI智慧学习系统 and exam coaching.
- Use `dp-product-new-customer-quote` for DP workload pricing and final DP quote output.
- Do not absorb general sales handbooks, unrelated products or broad objection-handling logic into this skill.

## Intake

Required for a useful draft:

- school, programme, degree level and target year/term;
- covered modules/tasks and known assessment details;
- target score/product preference;
- student risks and available brief/rubric/DDL materials.

Normalize all production inputs to `assets/schemas/intake.schema.json` and run `scripts/validate_intake.py`. Missing official details remain pending and must not become facts.

## Evidence

For course/module research, read `references/official_evidence.md`. Record official source year and URL. Separate official facts, estimates and customer-supplied facts.

## Output Contract

Read `references/output_contracts.md` and select exactly one:

- `D01`: pure DP client proposal;
- `D02`: DP module for a mixed DP + planning proposal;
- `D03`: DP Assessment Excel handoff for quote preparation.

Use fixed DP value content from `assets/templates/dp_fixed_value_modules.json`. Do not regenerate or paraphrase those fixed modules unless the user explicitly requests revised wording.

For a deterministic client HTML draft, prepare the contract JSON and run `scripts/build_dp_proposal.py`. It inserts the fixed value modules automatically.

Read `references/brand_visual_guidelines.md` only for branded HTML/PDF output. Read `references/sales_followup.md` only when WeChat follow-up copy is requested.

## Workflow

1. Normalize intake and validate material completeness.
2. Verify official programme/module/assessment evidence.
3. Diagnose DP fit using workload, target pressure, DDL concentration, task complexity and material gaps.
4. Select the DP product: 安心包, 卓越安心包 or 毕业无忧.
5. Select one output contract and fill only dynamic fields.
6. Reuse fixed value, assurance, process and team modules without rewriting.
7. If a price is requested, hand the final assessment workload to `dp-product-new-customer-quote`; do not calculate it here.
8. Render two strictly separated artifacts: a clean client HTML/PDF and the same-name `.internal.html/.internal.json` audit attachment. Export only the clean client HTML to PDF.
9. Add `课程与服务匹配` for every covered course: course code, course name, assessment form, workload and matched DP service.
10. If any fact, workload or scope is estimated/unreviewed, keep it in the internal attachment and use this exact reply prefix: `亲爱的学业规划师，您好！此次方案生成存在【预警提示】：`.

## Hard Rules

- DP scope and exam/test/quiz coaching remain separate.
- Client pages show no internal pricing formula, margin, negotiation strategy or internal version label.
- Client pages also show no source list, boundary note, warning block, quote status, trace ID or audit status.
- Do not promise guaranteed passing, guaranteed grades, zero risk,代考 or detection avoidance.
- A proposal with unknown brief/rubric/DDL remains a draft and lists required materials.
- Fixed value modules remain identical across equivalent proposals; customization belongs in student diagnosis, course map, risks, timeline and service focus.
- D01 follows fixed case 06. D02 is a compact module for fixed case 05 and must not expand into the full D01 layout.
