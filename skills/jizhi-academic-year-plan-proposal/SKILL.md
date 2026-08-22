---
name: jizhi-academic-year-plan-proposal
description: Generate client-facing annual or term academic execution plans with course priority, 陪跑/专业课 hours, AI智慧学习系统, public-sector concise plans, mixed DP plus planning structure, and planning-product quotes. Use for 全年学业规划、学业管家、课程规划、陪跑方案、专业课配置、AI智慧学习系统、对公服务匹配 or DP加陪跑混合方案. Do not use for the standalone eight-item planning report, pure DP proposals, or DP final-price requests.
---

# 极致学业规划年度方案

Generate Chinese academic-planning deliverables. This skill owns planning and陪跑 logic only. It must not calculate DP prices or create pure-DP proposals.

## Boundary

- Use this skill for academic planning, course priority, standard/custom planning hours, term timelines, daily/weekly/monthly execution, AI智慧学习系统 and planning-product quotes.
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

For stable production, normalize inputs to `assets/schemas/intake.schema.json`, validate with `scripts/validate_intake.py`, then render with `scripts/build_planning_proposal.py`.

## Evidence

Use official university sources for course facts. Separate official facts from planning judgments. Unknown weights, DDLs, word counts or briefs must remain `待Moodle/Canvas/Assessment Brief确认`.

## Output Routing

Select exactly one contract from `references/output_contracts.md`:

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
7. Generate the canonical HTML, export it to PDF and visually verify it. Keep the quote separate unless the user explicitly requests a merged file.

## Non-Negotiable Rules

- Every standard plan includes the six planning items: 学业画像、问题诊断与定位、目标差距分析、课程优先级排序、阶段行动建议、学业风险清单.
- `AI智慧学习系统` is a trackable learning space, not an assignment-writing tool.
- Proposal and quote are separate by default.
- Planning prices and DP prices must never share a formula.
- Client-facing text must not promise guaranteed grades or passing.
- Fixed template labels, value modules and disclaimers are copied unchanged; only student/course/timeline/service variables are generated.

## Assets

For branded outputs use the assets under `assets/brand/` and `assets/ip/`. IP images must remain unobstructed: no mask, overlay, dark filter or card covering the character.
