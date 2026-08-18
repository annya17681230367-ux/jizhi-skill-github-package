---
name: dp-product-new-customer-quote
description: Compile official university program or module assessment details and produce a client-ready coursework + quote deliverable. Use when given school/program/degree/entry year/target score (or package request) to extract assignment workload, credits, semester, risk, and output a formatted Excel with final quote while keeping pricing internals sealed.
---

# DP产品新客户报价（公开协作版）

## Overview
Produce one client-ready output that includes:
- Coursework table (课程信息 + 作业量 + 风险)
- Final quote block (only final numbers, no formulas)
- Formatted Excel in a single sheet

This public skill defines intake, data extraction, QA, and output format.
All pricing internals must be executed by private pricing service/tools only.

## Runtime Prerequisites (mandatory for final quote)
To produce final quote numbers, the runtime must be able to call an authorized private quote service. Public/shared copies of this skill must not contain real endpoint URLs, API keys, paid pricing files, or internal pricing formulas.

Required environment variables:
- `QUOTE_API_BASE` (provided privately by the quote administrator)
- `QUOTE_API_KEY` (sent via `X-API-Key` header)

Required local capability:
- Python `.xlsx` writer available (recommend `openpyxl`)
- If missing, install with: `python3 -m pip install openpyxl`
- If the repository script is available, use `scripts/quote_dp_api.py` for sealed quote requests. This script reads `.env` or shell environment variables and never prints the API key.

Hard stop rule:
- If quote API is unreachable, unauthorized, or returns no `final_price`, do not fabricate pricing.
- Continue with coursework extraction and Excel structure, but stop before final delivery and request pricing-channel recovery.

## Language Lock (mandatory)
Client-facing outputs must be Chinese by default:
- Excel sheet title, section titles, table headers, quote block labels, notes, and risk statements must all be Chinese.
- Keep official source names in original language when needed, but add Chinese explanation in adjacent text.
- If user explicitly requests English output, require explicit confirmation before switching language.

Hard stop:
- Do not deliver final Excel if core labels are English-only.
- Regenerate with Chinese headers/labels before delivery.

## Required Inputs
- School (university)
- Program/Department
- Degree level (UG/PGT/PGR)
- Entry year
- Either target score or package type
- Scope: full year or selected modules

Optional inputs:
- Module codes / module names (for partial-module coverage)
- Currency / rounding preference
- Special constraints affecting risk/delivery (urgent deadline, software limits, language support)

## Workflow

### 0) Intake confirmation (mandatory before research)
If key decision input is missing, ask and wait for confirmation:
- Is elective selection finalized?
  - If yes: request module codes/names (quote only covered modules).
  - If no: confirm whether to use an official sample pathway/representative year plan.
- Coverage scope: full year / semester / selected modules.
- Package input: target score or explicit package type.
- Year/Level clarification (mandatory):
  - 当前在读年级（仅背景信息）
  - 本次要做的目标年级/Level（用于选课和报价）
  - If conflict exists, always follow target year/level.

Hard stop:
- Do not generate final output if missing inputs would materially change module set, workload total, or quote.
- Stop when target covered year/level is ambiguous.

### 1) Find official sources
- Use official university pages, handbook/module catalog, and official policy pages.
- Match entry year first.
- Record source year + URL for each key fact.
- Check official academic calendar/term dates for target academic year; include only if exact dates are available.

### 2) Build covered module list
- Full-year scope: include full required module set for the target year/level.
- Partial scope: include only covered modules.
- Extract module credits and semester/teaching period.

### 3) Extract assessment workload
- Split each module into assessment components (one row per component).
- Extract weight, word count, duration, pages, task description.
- If official workload details are missing, estimate and mark clearly in `备注`.

### 4) Convert workload to words
Use fixed conversions:
- 1 hour exam ~= 1500 words
- 1 minute presentation ~= 100 words
- 1 page ~= 300 words

Requirements:
- Every assessment row must have a numeric word-equivalent.
- If duration is unknown, estimate by same-credit module workload references and document basis in `备注`.
- Keep same-credit workload totals roughly aligned unless official data clearly differs.

### 5) Determine package and pass benchmark
- If user provides package, use it.
- Else infer from target score:
  - Pass benchmark => 安心包
  - 60/65/70 => 卓越安心包
- Determine pass benchmark from official regulations for school + degree level + year.
- Distinguish UG vs PGT rules.
- For dissertation/thesis in 卓越安心包, cap promise to 60.

### 6) Pricing execution (sealed)
Use private pricing service/tooling only. Never embed or expose internal model details in this public skill.

Mandatory rules:
- Compute `chargeable_words_total` from the final coursework table.
- Request quote from private pricing channel using current final totals. Prefer the bundled helper when available:
  - `python3 scripts/quote_dp_api.py --payload-json '<payload>'`
  - If no helper is available, call the quote channel using environment variables only.
  - Endpoint: `POST $QUOTE_API_BASE/quote`
  - Headers:
    - `Content-Type: application/json`
    - `X-API-Key: $QUOTE_API_KEY`
  - Minimum payload:
    - `school`, `program`, `degree_level`, `target_year`, `scope`, `total_words`
    - Include `package_type` or `target_score` when available
  - Required response field: `final_price`
- If any workload row changes, invalidate prior quote and recompute.
- Final check: quote must match current `chargeable_words_total`; otherwise recalculate before delivery.

Confidentiality rules:
- Never reveal internal pricing logic or intermediate calculations.
- Never reveal `QUOTE_API_BASE`, `QUOTE_API_KEY`, request headers, raw secrets, or paid backend details.
- Output only package type, coverage, final price, and a short non-technical note.

### 7) Output format (client-facing)
Always include:
1. Basic info block
- 学校/专业/学位/入学年份/目标分数或套餐
- 专业概述
- 核心知识/技能/软件
- 学分要求
- 校历信息（目标学年学期起止时间；若官方无明确日期则省略）
- 重要提醒（如官方迟交处罚/缺考规则；若官方可得则必须展示）
- 信息源

2. Coursework table
- 序号 | 课程名称 | 学分 | 必修/选修 | 学期 | 作业 | 字数/时长（含换算） | 占比 | 作业简述 | 风险评估 | 判断依据 | 信息源 | 备注
- Sort: Semester 1 -> Semester 2 -> Full Year

3. Quote block (no formulas)
- 套餐类型
- 适用范围（课程作业 / 毕业论文）
- 最终报价
- 备注：根据内部报价机制计算，不展示计算过程

Source labeling:
- Include source year in labels when available (e.g., `Module Directory 2025/26`).
- `信息源` cells must be clickable hyperlinks.
- If source label is English, keep a Chinese field label and present as `中文说明（English Source Label）`.

### 8) Excel deliverable (required)
Generate one `.xlsx` single-sheet output:
- Top: basic info block (horizontal label/value layout)
- Middle: coursework table with styled header
- Bottom or top-right: quote block

Template style baseline:
- Header bold + light fill
- Practical column widths
- Wrap text for all content cells
- Keep info fields horizontal (label/value rows, merged value cells)
- `信息源` hyperlinks must remain clickable

## Quality Guardrails
- Do not fabricate official facts.
- Mark uncertain/estimated values clearly in `备注`.
- Do not include uncovered modules in quote for partial scope.
- Keep source years explicit where available.
- Never deliver a file where workload total changed but quote was not recomputed.

Final pre-delivery checklist:
- Every assessment row has numeric word-equivalent
- Quote recomputed from current final total
- 风险评估 has adjacent 判断依据
- 重要提醒 shown when official penalty/rule exists
- Source links are clickable and year-labeled where available
