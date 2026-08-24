---
name: jizhi-academic-year-plan-proposal
description: "Generate the single canonical academic-planning family: eight-item personalized reports, annual/term execution plans, client proposals, public-sector concise plans, planning quotes, and mixed DP plus planning structure. Use for 学业规划报告、客户学业方案、全年规划、陪跑、专业课配置、AI智慧学习系统、对公服务匹配、陪跑报价 or DP加陪跑混合方案. Do not use for pure DP proposals or standalone DP final-price requests."
---

# 极致学业规划年度方案

Generate Chinese academic-planning deliverables. This is the only public owner for personalized planning reports, annual execution plans, planning client proposals and planning-product quotes. It replaces `jizhi-academic-planning-report` and the planning/client-proposal portion of `jizhi-essay-customer-proposal`.

## Boundary

- Use this skill for eight-item diagnosis reports, academic planning, course priority, standard/custom planning hours, term timelines, daily/weekly/monthly execution, AI智慧学习系统, planning client proposals and planning-product quotes.
- For pure DP/安心包/卓越安心包 proposals, use `dp-proposal-designer`.
- For DP assessment pricing or a final DP price, use `dp-product-new-customer-quote`.
- For mixed DP + planning work, this skill owns the combined client structure; keep the two service scopes and quote engines separate.

Read `references/scenario_routing.md` only when the request mixes DP and planning or the product is ambiguous.

## Intake

Collect only fields that materially affect the plan:

- school, programme, degree level, target year/term and course list;
- official calendar, assessment and DDL evidence when available;
- student baseline, language, learning ability, weak areas and target;
- service period and standard/custom mode.

If the user does not explicitly request custom hours, use the standard package configuration in `references/service_packages.yaml`. Do not invent custom hours.

For stable production, normalize inputs to `assets/schemas/intake.schema.json`, validate with `scripts/validate_intake.py`, then render with `scripts/build_planning_proposal.py`. Every course must map to the shared `课程与服务匹配` fields: course code, course name, assessment form, workload and matched service.

## Evidence

Use `references/official_research_policy.md`. Prefer official information for the instruction date's calendar year; if unavailable, use the latest currently published official information and flag the year difference. Reuse verified school URLs from `assets/data/official_source_registry.json`, but revalidate stale facts. Every official fact needs its source URL. Unknown weights, DDLs, word counts or briefs remain pending.

## Output Routing

Select exactly one contract from `references/output_contracts.md`:

- `T00`: eight-item personalized planning report;
- `T01`: standard annual academic plan;
- `T02`: public-sector concise service-match plan;
- `T03`: standalone planning-product quote sheet;
- `T05`: mixed DP + planning plan.

Do not read every template case. Use only the selected contract and its named template asset.

Read additional references only when required:

- course classification, execution rhythm or AI system: `references/service_logic.md`;
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
7. Generate two strictly separated artifacts: the clean client HTML/PDF and the same-name `.internal.html/.internal.json` audit attachment. Export only the clean client HTML to the customer PDF.
8. Put sources, missing facts, model estimates, warnings, contract/version identifiers, quote trace and review status only in the internal attachment. If warnings exist, the conversation reply must include exactly: `亲爱的学业规划师，您好！此次方案生成存在【预警提示】：（预警提示内容）`.

## Non-Negotiable Rules

- Every standard plan includes the six planning items: 学业画像、问题诊断与定位、目标差距分析、课程优先级排序、阶段行动建议、学业风险清单.
- `AI智慧学习系统` is a trackable learning space, not an assignment-writing tool.
- Proposal and quote are separate by default.
- Planning prices and DP prices must never share a formula.
- Client-facing text must not promise guaranteed grades or passing.
- Fixed template labels, value modules and disclaimers are copied unchanged; only student/course/timeline/service variables are generated.
- Never place internal sources, boundary notes, warnings, version labels, quote trace IDs or review status in the client artifact.
- Never suppress ambiguity. Missing official facts, estimated workload, unmatched pricing matrix, unreviewed estimates, stale sources and out-of-scope requests must become warnings in the internal audit artifact and the reply.
- Visual routing is fixed: T01 follows fixed case 01, T02 case 02, T03 case 03 and T05 case 05. Do not replace them with a generic long-form document.

## Assets

For branded outputs use the assets under `assets/brand/` and `assets/ip/`. IP images must remain unobstructed: no mask, overlay, dark filter or card covering the character.
