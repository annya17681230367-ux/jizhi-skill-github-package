# DP Pricing Rules

Use this reference whenever the user asks for DP价格、报价、报价单、费用、总价、原价、折后价、内部报价、客户报价, or when a DP proposal explicitly asks to include a quote.

## Why DP quote generation used to stall

The DP proposal skill previously said "include quote only if requested or enough price direction exists" but did not define:

- what counts as enough price direction;
- what to do when exact price files are not bundled;
- how to separate DP quote logic from 学业规划陪跑 quote logic;
- what fields an internal quote must contain.

As a result, the model often stopped and asked for more pricing input instead of producing a reviewable internal quote draft.

## Non-Negotiable Boundary

DP quote logic is separate from 学业规划陪跑 quote logic.

- DP covers assignment/project/presentation/dissertation/capstone management and quality-control work.
- 学业规划陪跑 covers course planning, specialist teaching hours, planning/execution hours, AI智慧学习系统, and weekly learning execution.
- If both products appear in one request, calculate DP and陪跑 in separate blocks, then show a combined total only after both subtotals are visible.

## Quote Decision Flow

1. If the user asks for a DP proposal only, do not include price unless requested.
2. If the user asks for DP报价/报价单/价格:
   - Prefer using the `dp-product-new-customer-quote` skill and authorized private quote channel when available.
   - Produce an internal quote sheet or internal quote logic first unless they explicitly ask for a client-facing quote.
   - Do not stop merely because exact pricing files are missing.
   - Use available inputs to create a reviewable quote draft with `待价格文件核对` flags where needed.
3. If official or internal DP price files are provided:
   - Read them first.
   - Use their unit prices, package tiers, discounts, and payment rules.
4. If no DP price file is available:
   - Use a quote placeholder table instead of inventing final prices.
   - Still classify workload and scope so sales can fill prices quickly.
5. If the user gives a target price or discount:
   - Back-calculate only when explicitly requested.
   - Label it as user-provided/inferred.

## Required Internal Quote Fields

Every DP internal quote draft must include:

- 学校 / 专业 / 学期 / 产品名称.
- 课程数量 and course list.
- DP product type: `DP安心包`, `DP卓越安心包`, `毕业无忧`, or custom DP scope.
- Covered assessment tasks per course.
- Excluded tasks: especially exams, tests, quizzes, participation, or non-DP tutoring.
- Workload basis: words/pages/slides/presentation/video/capstone/dissertation.
- Risk level: 低 / 中 / 中高 / 高.
- Pricing status:
  - `可报价` when price file or explicit pricing direction exists.
  - `待价格文件核对` when scope is clear but unit price is unavailable.
  - `需补材料` when brief/rubric/DDL materially changes workload.
- 原价.
- 折扣逻辑.
- 折后价.
- Assumptions and re-quote triggers.

## Authorized Quote Channel Integration

When the installed environment has `dp-product-new-customer-quote` and quote environment variables, DP final quotes should use the sealed quote channel instead of local/invented formulas. Public/shared skill packages must not include real endpoint URLs, API keys, paid pricing files, or internal pricing formulas.

Required environment variables:

- `QUOTE_API_BASE`
- `QUOTE_API_KEY`

Health check and quote request are executed only on authorized administrator machines. Do not place real command examples with endpoint URLs or API keys in public collaboration materials.

Preferred execution when this repository package is available:

```bash
python3 scripts/quote_dp_api.py --payload-json '<payload-json>'
```

The helper reads `.env` or shell environment variables, calls the quote endpoint, validates `final_price`, and prints only the sealed API response.

Required response field:

- `final_price`

Client-facing output may show:

- `package_type`
- `scope`
- `final_price`
- `currency`
- API note if it is non-technical

Do not show:

- internal price formulas
- API key or endpoint URL
- raw secrets
- internal calculations

If the API is unavailable or unauthorized:

- Do not fabricate final price.
- Continue producing coursework/assessment scope and quote-ready table.
- Mark final amount as `待报价通道恢复后计算`.

## Client Quote Fields

A client-facing DP quote may show:

- Product name.
- Covered courses/tasks.
- Service period.
- Original price.
- Discount or package benefit.
- Final price.
- Payment method and validity if supplied.
- Scope boundary and re-quote triggers.

Do not show:

- Internal formula.
- Margin.
- Bottom line.
- Negotiation room.
- Internal “why this price” notes.

## DP Scope Classification

Use this scope classification before pricing:

| Task Type | DP Included? | Notes |
|---|---|---|
| Essay / report / reflective writing | Usually included | Count by word count, complexity, rubric, and sources. |
| Group report / group project | Usually included | Include coordination risk and group deliverables. |
| Presentation / pitch / video | Usually included | Count slides, script, Q&A, rehearsal, and group division. |
| Dissertation / capstone / portfolio | Included as special/high scope | Quote separately or as `毕业无忧`/`卓越安心包`. |
| Quiz / test / final exam | Not DP by default | Route to tutoring/陪跑 if requested. |
| Weekly participation | Usually pending | Include only if contract says participation preparation is covered. |

## Quote Sheet Structure

Use this structure for DP quote sheets:

1. Quote header:
   - Student/program summary.
   - Product type.
   - Service period.
2. Course/task table:
   - Course.
   - Assessment task.
   - Weight.
   - Workload.
   - DP service scope.
   - Included/excluded.
   - Risk.
   - Pricing status.
3. Pricing table:
   - DP assignment/project package subtotal.
   - Dissertation/capstone subtotal if any.
   - Presentation/project management subtotal if separately priced.
   - Discount/package benefit.
   - Original price.
   - Discounted price.
4. Boundary notes:
   - Exams/tests excluded unless separately purchased.
   - Latest Moodle/Canvas/brief/rubric may change scope.
   - Contract terms control final service guarantee.
5. Verification:
   - Course count matches proposal.
   - Included/excluded tasks are visible.
   - Original price and discounted price reconcile.

## If Mixed With 学业规划陪跑

For mixed方案:

- Create two quote sections:
  - `DP报价逻辑`.
  - `学业规划陪跑报价逻辑`.
- Never use陪跑 standard package prices for DP tasks.
- Never use DP package language for specialist teaching or陪跑课.
- Combined total is allowed only after both subtotals are shown.

## Must-Continue Rule

When the user asks for DP报价 and some information is missing, continue with a draft instead of stopping:

- Fill known course/task data.
- Mark unknown prices as `待价格文件核对`.
- Mark unknown briefs/rubrics as `需补材料`.
- Give the exact missing materials list at the bottom.

Only ask a blocking question when the user asks for a final client-facing price and there is no price file, no target price, and no approved pricing rule.
