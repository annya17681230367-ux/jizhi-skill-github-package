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
- specialist + planning lesson counts;
- original unit price and original subtotal;
- applicable approved discount;
- discounted subtotal and final total;
- a `报价速查目录与资料` section that shows the approved standard-package combinations, including course mix, lesson mix, component-only original total, approved standard price and saving amount;
- the selected course mix and whether it matches the approved matrix; if unmatched, show component original total and mark final discounted price as `待人工核价`;
- scope and validity notes.

## Mixed Product Rule

For DP + planning work:

- calculate planning lines here;
- request DP pricing through `dp-product-new-customer-quote`;
- present two independent subtotals and an arithmetic combined total only when requested;
- never derive one product price from the other.

## Verification

Before export, recompute line subtotals, original total, discount and final total. Verify displayed course counts and lesson counts against the confirmed plan.
