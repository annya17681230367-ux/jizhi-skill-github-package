---
name: dp-product-new-customer-quote
description: Produce a DP-only assessment workload workbook and final sealed price. Use for DP报价, DP产品价格, 安心包报价, Assessment报价表, 作业量报价, 课程考核加DP报价, or requests that ask only for a final DP price/Excel. Do not use for DP client proposal design, annual planning, tutoring-hour pricing, or mixed-product narrative.
---

# DP Product New Customer Quote

## Boundary

This skill owns only:

1. Official assessment evidence and chargeable workload.
2. DP quote payload construction.
3. Authorized private quote request.
4. Chinese assessment-and-quote Excel output.

Route DP proposal pages to `dp-proposal-designer`. Route annual planning, exam tutoring, planning lessons, or their prices to `jizhi-academic-year-plan-proposal`. In mixed products, quote only the DP portion and return the result to the owning proposal skill.

## Inputs

Require school, program, degree level, target academic year, covered scope, and either confirmed modules or an explicitly approved official pathway. Also collect target score or package type when available.

If module coverage or target level would change workload materially, stop and request that missing input. Do not silently expand scope.

## Workflow

1. Research official university sources for the target year. Record source URL and source year beside every assessment fact.
2. Build one row per assessment component using `assets/schemas/assessment_quote.schema.json`: course code and name, term, assessment type, weight, official workload, quote-equivalent words, requirement, risk, evidence, source and note.
3. Convert workload only when needed for the quote payload. Use the conversion policy returned by the authorized quote service or the approved internal input; do not invent private pricing logic in this skill.
4. Validate the final covered rows and total workload.
5. Build the complete quote workbook. Use `--request-quote` only on an authorized machine:

```bash
python3 scripts/build_quote_workbook.py assessment.json quote.xlsx --request-quote
```

For internal review without an API call, omit `--request-quote`; the workbook will show `待授权报价`. If any covered row changes, invalidate the old quote and call again.

6. Produce the selected contract in [output_contracts.md](references/output_contracts.md).

## Hard Stops

- No official evidence: mark the field pending; never fabricate it.
- Missing `QUOTE_API_BASE`, `QUOTE_API_KEY`, or `final_price`: do not produce a final price.
- Never print, embed, upload, or explain API credentials, endpoint URLs, paid rules, intermediate pricing formulas, or raw backend responses containing private fields.
- Client output is Chinese by default and shows only package, coverage, original price when returned, discount price, and a short non-technical note.

## Delivery Check

- Covered modules match the confirmed scope.
- Each assessment row has a source and evidence status.
- Quote total matches the final workload.
- Links are clickable and source years are visible.
- No planning/tutoring hours or DP proposal copy appears in this output.
