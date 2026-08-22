# Planning Product Quote Rules

Read only when the user explicitly requests a planning/陪跑 quote. This file never prices DP work.

## Preconditions

- The proposal or covered course list is confirmed.
- Course classification is final.
- Standard hours come from `service_packages.yaml`; custom hours require an explicit custom instruction.
- Use only a separately authorized private planning-pricing source. Public skill packages contain no price list or internal formula.
- If the private source is unavailable, produce a scope-and-hours review sheet marked `待内部核价`; do not invent a final price.

## Required Output

Use contract `T03` in `output_contracts.md` and show:

- each course/service line;
- 重点/非重点/custom classification;
- specialist + planning lesson counts;
- original unit price and original subtotal;
- applicable approved discount;
- discounted subtotal and final total;
- scope and validity notes.

## Mixed Product Rule

For DP + planning work:

- calculate planning lines here;
- request DP pricing through `dp-product-new-customer-quote`;
- present two independent subtotals and an arithmetic combined total only when requested;
- never derive one product price from the other.

## Verification

Before export, recompute line subtotals, original total, discount and final total. Verify displayed course counts and lesson counts against the confirmed plan.
