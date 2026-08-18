# Pricing And Quote Rules

Use this reference for every 报价单, price, package comparison, 原价, 折后价, or quote request.

## Required Pricing Materials
Public/shared skill packages must not include internal paid pricing materials, API keys, endpoint URLs, bottom-line formulas, discount tables, or negotiation rules.

Before calculating any final quote, use only pricing materials supplied privately in the current conversation or available on the authorized administrator machine. If the pricing material is unavailable, produce a quote-ready table and mark the final amount as `待管理员报价`.

## Proposal vs Quote Boundary
- Default first-draft方案 generation is text/Markdown, not PDF, unless the user explicitly asks for a final rendered PDF.
- Final confirmed方案 and报价单 are separate files by default.
- The方案 file must not mention any price, quote, amount, discount, payment, promotion, or offer unless the user explicitly asks to merge quote into proposal.
- Generate a quote sheet only after the方案 is confirmed or the user issues a separate quote instruction based on a confirmed方案.
- If the user asks for方案+报价 in one turn, produce the text draft方案 first and separate quote logic/checklist; generate final PDF quote only after confirmation unless the user explicitly says the方案 is already confirmed.

## Quote Routing
Choose the quote method flexibly, but always according to authorized pricing materials:

1. `标准套餐报价`
   - Default for 学业规划陪跑 when the user has not explicitly requested custom hours.
   - Use authorized pricing rules for course count, degree level, service period,重点/非重点 classification, and required components.

2. `门数折扣报价`
   - Use when authorized pricing materials include course-count/package discounts.
   - The discount may vary by number of courses, service period, or package type. Do not assume a fixed four-course discount.
   - Show the course-count tier, discount source, original price, discount amount/rate, and final price.

3. `定制方案报价`
   - Use only when the user explicitly says定制方案/定制课时 or provides exact per-course hours/components.
   - Calculate from component prices and label each line formula.

4. `混合方案报价`
   - Use when DP and学业规划陪跑 appear together.
   - Calculate DP and陪跑 separately using their own pricing boundaries, then apply only the combined/package discount supported by authorized materials or explicitly provided by the user.
   - Never blend DP and陪跑 formulas into one unexplained total.

## Standard Package Rule
Unless the user explicitly requests `定制方案`, `定制课时`, or provides exact custom hours, all proposals and quotes use the standard package rule from the questionnaire.

Current standard package defaults, to be verified against authorized materials each time:
- 重点课程: 6节专业课 + 10节规划执行/陪跑课.
- 非重点课程: 2节专业课 + 8节规划执行/陪跑课.

For standard packages:
- Classify each course as重点 or 非重点 based on assessment risk, DDL density, student weakness, target, and course content.
- Do not invent bespoke per-course hours.
- Quote only when authorized unit prices are available. If not available, show course classification and total hours, then mark amount as `待管理员报价`.

## Custom Plan Rule
Use custom pricing only when the instruction explicitly says定制方案/定制课时 or gives custom per-course hours.

For custom plans:
- Use the actual professional-hour and planning/execution-hour split provided or justified by the plan.
- Calculate with authorized unit prices only.
- Clearly label every pricing logic line: service mode, course count, months, unit price, formula, original price, discount rule, and final discounted price.

## Required Quote Fields
Every quote sheet must show:
- 报价版本: 内部报价版 or 客户报价版.
- 对应方案: proposal file/name/date/version.
- 服务模式: 标准套餐 or 定制方案.
- 课程 classification: 重点/非重点 or custom reason.
- 每门课服务内容 and workload basis: assessment components, DDL/brief workload, DP/陪跑/专业课 coverage.
- 每门课课时: 专业课 + 规划执行/陪跑课.
- 课程管理费 formula.
- AI智慧学习系统 formula.
- 学业诊断与规划 formula.
- Optional add-ons only if included: 每日答疑窗口, VIP响应升级, 家长月度汇报, 夜间/节假日/紧急服务.
- 原价.
- 折扣/优惠逻辑. If no discount is provided, show `暂无折扣` and make折后价 equal原价.
- 折后价.
- 付款/有效期 note if supplied by the user.

## Discount Rule
- Always provide original price and discounted price.
- Course-count/package discounts must come from authorized pricing materials or explicit user instruction. Do not invent a discount rate.
- If the user gives a target final price, back-calculate the original price only when they explicitly ask to do so; label the inferred discount rate.
- If no discount is specified, do not invent one: 原价 = 折后价, 折扣 = 暂无折扣.

## Verification Before Export
Before exporting a quote PDF:
1. Recompute totals independently from the table.
2. Check that course-hour subtotals equal total professional and planning/execution hours.
3. Check that monthly components use the correct course count and service months.
4. Check that original price, discount, and final discounted price reconcile.
5. Render PDF previews and inspect that logo, IP image, tables, totals, and footnotes do not overlap.
