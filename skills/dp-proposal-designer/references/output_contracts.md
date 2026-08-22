# DP Proposal Output Contracts

Select exactly one contract. Dynamic sections are customized; fixed value modules come from `assets/templates/dp_fixed_value_modules.json`.

Every proposal contract contains `课程与服务匹配`: `课程名称 | 课程代码 | 课程考核形式 | 课程工作量 | 匹配服务`.

## D01 Pure DP Client Proposal

Program template key: `D01` in `assets/templates/template_contracts.json`.

Fixed order:

1. Cover - dynamic school/program/term/target/product.
2. Student situation and DP fit conclusion - dynamic.
3. Official course/assessment map - dynamic and sourced.
4. Risk and workload summary - dynamic.
5. Recommended DP product and course/task service focus - dynamic.
6. DP core value - fixed module.
7. DP assurance process - fixed module.
8. Included/excluded scope - fixed boundary plus dynamic task mapping.
9. Execution timeline - dynamic dates/tasks.
10. Team and quality control - fixed module.
11. Materials required and next action - fixed labels, dynamic list.
12. Quote status only when requested; final value comes from the DP quote skill.

No planning/陪跑 lesson allocation appears in D01.

## D02 DP Module For Mixed Plan

Owner of the combined document: `jizhi-academic-year-plan-proposal`.

Provide only:

- DP-covered assessment tasks;
- fixed DP core value and assurance process;
- DP timeline/owner;
- included/excluded scope;
- DP quote handoff status.

Do not add planning hours, AI智慧学习系统, exam coaching or planning prices.

## D03 DP Assessment Excel Handoff

Use when the next step is DP pricing.

Required columns:

`课程代码 | 英文课程名 | 中文课程名 | Assessment | 类型 | 占比 | 字数/时长 | DDL/周次 | 个人/小组 | 官方来源 | 备注`

Rules:

- one assessment component per row;
- every row maps to a course code and name;
- English task descriptions receive a Chinese explanation;
- unknown fields remain pending;
- no final price is calculated by this skill.
