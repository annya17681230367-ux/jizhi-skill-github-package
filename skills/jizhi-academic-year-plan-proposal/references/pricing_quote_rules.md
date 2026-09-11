# Planning Product Quote Rules

Read only when the user explicitly requests a planning/陪跑 quote. This file never prices DP work.

## Preconditions

- The proposal or covered course list is confirmed.
- Course classification is final.
- Standard hours come from `service_packages.yaml`; custom hours require an explicit custom instruction.
- Use the separately installed `jizhi-planning-pricing-private` add-on through `scripts/build_planning_quote.py`. Public skill packages contain no price list or internal formula.
- If the private source is unavailable, produce a scope-and-hours review sheet marked `待内部核价`; do not invent a final price.
- Standard matrix combinations and nonstandard periods follow the private add-on warnings. A warning cannot be removed merely to make the quote look complete.

## Required Output

Use contract `T03` in `output_contracts.md` and show:

- each course/service line;
- 重点/非重点/custom classification;
- subject type and professional direction when the plan is custom or discipline-based;
- specialist + planning lesson counts;
- matched service and component services;
- original unit price and original subtotal;
- applicable approved discount;
- discounted subtotal and final total;
- a `报价速查目录与资料` section that shows the approved standard-package combinations, including course mix, lesson mix, component-only original total, approved standard price and saving amount;
- the selected course mix and whether it matches the approved matrix; if unmatched, show component original total and mark final discounted price as `待人工核价`;
- scope and validity notes.

## Calculation Logic By Quote Type

Do not hard-code course names, student cases or example prices into the quote logic. Every quote must be calculated from the current student's course list, course classification, requested service mode and authorized pricing source.

### Standard Package Quote

Use when the student selects an approved standard package or when the course mix matches a published standard matrix.

1. Count courses by classification: `key_courses` and `non_key_courses`.
2. Load the approved standard package matrix from the private pricing source.
3. Match the student's course mix against the quote quick-reference catalog, such as `1重点`, `1非重点`, `1重点+1非重点`, `2重点+2非重点`, `3重点+3非重点`, or any newly approved catalog row returned by the private source.
4. If a catalog row is matched, read that row's original price, discount/saving, discounted standard package price and lesson/service mix.
5. Display the selected catalog row in the quote sheet, including original price, discount or saving amount, discounted price and whether it is an exact standard-package match.

If no exact standard matrix exists, do not invent the package discount. Switch to custom quote handling or mark the discounted price as `待内部核价`.

### Custom Lesson Quote

Use when the user specifies nonstandard lesson counts, light-pacing caps, unusual service months, or a course mix not covered by the standard matrix.

1. Read each course line from the current proposal.
2. For each course, record classification, specialist lesson count, pacing/planning lesson count, subject type, professional direction and matched service.
3. Validate service constraints, such as per-course pacing caps and professional-lesson dominance when requested.
4. Read the authorized unit price for each course from the pricing source by subject type and professional direction. Use the matched professional lesson unit price and pacing/planning lesson unit price to calculate each course's original subtotal.
5. Component services are counted once by default across the custom plan, unless the user explicitly asks to charge a component repeatedly per course or per term.
6. Match the course count or service mix to any approved custom discount rule returned by the private pricing source.
7. Display each course's professional lesson subtotal, pacing/planning lesson subtotal, component-service share when applicable, original subtotal, approved discount status and discounted subtotal.
8. Display total original amount, total discount, final total and warning status.

If the private source says the custom mix is unmatched or pending review, the quote sheet must show `待内部核价` or `待确认折扣`, not a manually guessed discount.

### Mixed DP + Planning Quote

Use when the proposal includes both DP and planning/陪跑/professional lessons.

1. Calculate planning/professional/pacing lines with this planning quote route.
2. Calculate DP assessments with `dp-product-new-customer-quote`.
3. Show per-course planning/professional/pacing prices and per-course DP matches in one quote table when DP is present. For each course show: planning original price, planning discount, planning discounted price, DP service matched or not, single-course DP price when returned, and course subtotal.
4. Show two independent subtotals: planning subtotal and DP subtotal.
5. Show total lesson count, total service match summary, total original amount, total discount and final combined amount.
6. Show a combined total only as arithmetic addition of the approved planning subtotal and approved DP subtotal.
7. Keep warnings separate: planning warnings for course mix/lesson pricing; DP warnings for Brief, rubric, DDL, workload and assessment evidence.

Never use a planning discount to discount DP, and never use a DP final price to infer planning price.

## Mixed Product Rule

For DP + planning work:

- calculate planning lines here;
- request DP pricing through `dp-product-new-customer-quote`;
- present two independent subtotals and an arithmetic combined total only when requested;
- never derive one product price from the other.

## Verification

Before export, recompute line subtotals, original total, discount and final total. Verify displayed course counts and lesson counts against the confirmed plan.
