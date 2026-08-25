# Academic Planning Output Contracts

Select exactly one contract. Fixed labels and fixed value modules must be reused unchanged. Generate only fields marked `VARIABLE`.

Every contract contains a compact `课程与服务匹配` module with: `课程名称 | 课程代码 | 课程考核形式 | 课程工作量 | 匹配服务`. Workload basis, warnings and official source details remain in the internal audit artifact.

## T00 Personalized Eight-Item Planning Report

Owner: `jizhi-academic-year-plan-proposal`.

Fixed order:

1. Student and target context.
2. Eight items: 个人学业画像、核心问题诊断、目标差距分析、定制路径图、阶段行动节点、课程优先级、学业风险清单、执行与支持建议.
3. 课程与服务匹配.
4. Internal-only sources, pending materials and warnings.

No quote unless the user separately requests T03.

## T01 Standard Annual Academic Plan

Owner: `jizhi-academic-year-plan-proposal`.
Program template key: `T01` in `assets/templates/template_contracts.json`.

Fixed order:

1. Cover and positioning - VARIABLE school/program/year/target.
2. Six planning items - REQUIRED fixed labels: 学业画像、问题诊断与定位、目标差距分析、课程优先级排序、阶段行动建议、学业风险清单.
3. Official course assessment summary - VARIABLE.
4. Course priority and standard/custom hours - VARIABLE classification; hours from configuration.
5. Annual/term timeline - VARIABLE dates and courses.
6. Daily/weekly/monthly execution - fixed service logic, VARIABLE dates/tasks.
7. AI智慧学习系统 - fixed positioning/functions, VARIABLE course examples.
8. Team roles and expected effect - fixed roles, VARIABLE student-specific effect.
9. Internal-only sources, pending materials and disclaimer - VARIABLE sources/missing facts.

No price appears in T01.

Hard gate: fixed case 01, exactly 2 pages, PingFang SC CSS stack, complete logo and unobstructed IP on page 1, course/timeline/AI execution modules on page 2, and passing `.preflight.json` after PNG review.

## T02 Public-Sector Concise Service-Match Plan

Owner: `jizhi-academic-year-plan-proposal`.
Program template key: `T02` in `assets/templates/template_contracts.json`.

Limit: 1-2 pages.

Fixed order:

1. Basic course/student context.
2. Compact official assessment summary.
3. Course-to-service match.
4. Stage timeline.
5. Daily/weekly/monthly service actions.
6. AI智慧学习系统 role.
7. Expected effect and material boundary.

No logo, price, internal version label or long raw DDL wall unless explicitly requested.

## T03 Standalone Planning Quote

Owner: annual skill using `pricing_quote_rules.md`.
Program template key: `T03` in `assets/templates/template_contracts.json`.

Required fixed fields:

- product/course/service line;
- course classification;
- specialist and planning lesson count;
- original price;
- discount rule/discounted price;
- final total;
- scope note and validity note.

Do not include DP work. DP quotes belong to the DP quote skill.

## T05 Mixed DP + Planning Plan

Owner: annual skill. DP content is supplied by `dp-proposal-designer`.
Program template key: `T05` in `assets/templates/template_contracts.json`.

Fixed order:

1. Student/course context.
2. Official assessment map.
3. Product split and responsibility boundary.
4. DP scope and fixed DP value module.
5. Planning/exam-support scope and lesson allocation.
6. Combined timeline with separate owners.
7. Expected effect and student responsibilities.
8. Two separate quote blocks only when explicitly requested.

Never merge the two price calculations.
