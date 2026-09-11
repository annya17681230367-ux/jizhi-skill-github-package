---
name: jizhi-academic-year-plan-proposal
description: "Generate the single canonical academic-planning family: eight-item personalized reports, annual/term execution plans, client proposals, public-sector concise plans, planning quotes, and mixed DP plus planning structure. Use for 学业规划报告、客户学业方案、全年规划、陪跑、专业课配置、AI智慧学习系统、对公服务匹配、陪跑报价 or DP加陪跑混合方案. Do not use for pure DP proposals or standalone DP final-price requests."
---

# 极致学业规划年度方案

Generate Chinese academic-planning deliverables. This is the only public owner for personalized planning reports, annual execution plans, planning client proposals and planning-product quotes. It replaces `jizhi-academic-planning-report` and the planning/client-proposal portion of `jizhi-essay-customer-proposal`. Customer-facing planning outputs should use the UCL-style project-management visual master unless a fixed legacy contract or user-supplied reference requires another style.

## Boundary

- Use this skill for eight-item diagnosis reports, academic planning, course priority, standard/custom planning hours, term timelines, daily/weekly/monthly execution, AI智慧学习系统, planning client proposals and planning-product quotes.
- When the user asks for a student/family-facing customer proposal, branded sales proposal, "展示服务价值", "美观PDF", "客户版方案", or says to break out of the fixed template logic, use the client-support proposal route in `references/client_support_proposal.md` and `scripts/build_client_support_proposal.py`. This route is not bound to fixed T01 page counts.
- For pure DP/安心包/卓越安心包 proposals, use `dp-proposal-designer`.
- For DP assessment pricing or a final DP price, use `dp-product-new-customer-quote`.
- For mixed DP + planning work, this skill owns the combined client structure; keep the two service scopes and quote engines separate.
- For mixed DP + light-pacing customer proposals, follow the UCL-style project-management pattern in `references/planning_output_taxonomy.md`: professional lessons dominate, pacing is capped per course when requested, DP modules are shown separately from course/exam support, and pricing is delivered as a separate quote artifact unless the user asks otherwise.

Read `references/scenario_routing.md` only when the request mixes DP and planning or the product is ambiguous.

## Intake

Collect only fields that materially affect the plan:

- school, programme, degree level, target year/term and course list;
- official calendar, assessment and DDL evidence when available;
- student baseline, language, learning ability, weak areas and target;
- service period and standard/custom mode.

If the user does not explicitly request custom hours, use the standard package configuration in `references/service_packages.yaml`. Do not invent custom hours.

For stable production, normalize inputs to `assets/schemas/intake.schema.json`, validate with `scripts/validate_intake.py`, then render with `scripts/build_planning_proposal.py`. Every course must map to the shared `课程与服务匹配` fields: course code, course name, assessment form, workload and matched service.

T00/T01/T02/T03/T05 use fixed generators. Fixed headings, service copy, role copy, section order, page count, logo/IP policy and typography cannot be rewritten; only validated student, course, evidence, date, service and authorized price fields are variable. Client-support proposals are a separate flexible route and must not be forced into the T01 exactly-three-page contract.

## Evidence

Use `references/official_research_policy.md`. Prefer official information for the instruction date's calendar year; if unavailable, use the latest currently published official information and flag the year difference. Reuse verified school URLs from `assets/data/official_source_registry.json`, but revalidate stale facts. Every official fact needs its source URL. Unknown weights, DDLs, word counts or briefs remain pending.

## Output Routing

Select exactly one contract from `references/output_contracts.md`:

- `T00`: eight-item personalized planning report;
- `T01`: standard annual academic plan;
- `T02`: public-sector concise service-match plan;
- `T03`: standalone planning-product quote sheet;
- `T05`: mixed DP + planning plan.
- `CLIENT_SUPPORT`: flexible branded student/family-facing proposal focused on service architecture, course risk, course-to-service matching, lesson mix and year execution. Use only when the user explicitly wants a customer-facing proposal instead of the fixed report contracts.

Do not read every template case. Use only the selected contract and its named template asset.

Read additional references only when required:

- course classification, execution rhythm or AI system: `references/service_logic.md`;
- customer-facing branded proposal design and output classification: `references/client_support_proposal.md` and `references/planning_output_taxonomy.md`;
- planning-product quote: `references/pricing_quote_rules.md`;
- branded HTML/PDF: `references/brand_visual_spec.md`;
- final verification: `references/quality_check.md`.

## Workflow

1. Normalize the intake and mark missing facts.
2. Verify official course and calendar evidence.
3. Diagnose the student-specific gap and classify courses as重点/非重点.
4. Apply standard hours from `service_packages.yaml`, unless custom mode is explicit.
5. Select one output contract and fill only its variable fields.
6. Reuse fixed value modules and fixed labels from the contract/template; do not rewrite them.
7. Generate the clean client HTML with `build_planning_proposal.py`, then export only that HTML through `export_pdf.py` using HeadlessChrome/Skia. Do not rebuild the customer layout with ReportLab.
8. `export_pdf.py` must create rendered PNG pages and a same-name `.preflight.json`. Inspect every PNG, then run `preflight_pdf.py ... --visual-reviewed`. Do not deliver unless `preflight_pass=true`.
9. Generate the same-name `.internal.html/.internal.json` audit attachment. Put sources, missing facts, model estimates, warnings, contract/version identifiers, quote trace and review status only in the internal attachment. If warnings exist, the conversation reply must include exactly: `亲爱的学业规划师，您好！此次方案生成存在【预警提示】：（预警提示内容）`.

## Client-Support Proposal Route

Use this route for polished student/family-facing proposals where the goal is to explain the service clearly and convincingly. It is optimized for sales and client understanding, not internal audit density.

- Use `references/planning_output_taxonomy.md` to classify the output as standard, custom, mixed DP + planning, planning quote or public-sector concise plan before writing.
- Normalize inputs to `assets/schemas/client_support_proposal.schema.json`.
- Render with `scripts/build_client_support_proposal.py`.
- Keep course risks, course-service matching, lesson counts and stage support specific.
- Avoid headings such as "给学生的价值" or generic value labels. Let value be visible through service structure, course risk handling and deliverables.
- Remove contrastive sales copy such as "我们不会只给家长一句..." or other lines that criticize a weaker service model.
- Keep pacing/coaching lessons limited when requested; when the user says "陪跑课每门最多2-3节课，其余安排专业课", enforce per-course pacing lessons <= 3 and show professional lesson percentage.
- Do not include pricing unless the user asks for quote content.
- Client copy may include a concise "待确认资料" list, but must not expose internal audit traces, model-estimate wording, private sources or unreleased pricing.
- Export to PDF with HeadlessChrome/Skia or a visually equivalent renderer, render pages to PNG, and inspect representative pages before delivery. The page count is flexible; visual quality and client readability are the gate.

## Non-Negotiable Rules

- Every standard plan includes the six planning items: 学业画像、问题诊断与定位、目标差距分析、课程优先级排序、阶段行动建议、学业风险清单.
- `AI智慧学习系统` is a trackable learning space, not an assignment-writing tool.
- Proposal and quote are separate by default.
- Planning prices and DP prices must never share a formula.
- Client-facing text must not promise guaranteed grades or passing.
- Fixed template labels, value modules and disclaimers are copied unchanged; only student/course/timeline/service variables are generated.
- Never place internal sources, boundary notes, warnings, version labels, quote trace IDs or review status in the client artifact.
- Never suppress ambiguity. Missing official facts, estimated workload, unmatched pricing matrix, unreviewed estimates, stale sources and out-of-scope requests must become warnings in the internal audit artifact and the reply.
- Visual routing is fixed: T00 follows fixed case 00, T01 case 01, T02 case 02, T03 case 03 and T05 case 05. Do not replace them with a generic long-form document.
- The customer PDF is incomplete until its `.preflight.json` says `preflight_pass=true`. Wrong page count, missing font contract, missing rendered PNGs, unreviewed PNGs, internal evidence leakage, forbidden price leakage or guaranteed-grade claims are hard failures.
- Every final delivery reply must reproduce `acceptance_declaration` from the passing preflight file. Missing this declaration means the delivery is incomplete.

## Assets

For branded outputs use the assets under `assets/brand/` and `assets/ip/`. IP images must remain unobstructed: no mask, overlay, dark filter or card covering the character.
