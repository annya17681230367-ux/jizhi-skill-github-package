# Jizhi Skill Package 2.1.0

## Stable product boundaries

1. `jizhi-academic-year-plan-proposal`
   - Annual academic planning, course companionship, AI learning system, planning quotes, and mixed DP + companionship proposals.
2. `dp-proposal-designer`
   - Client-facing DP proposals with fixed value, process, evidence, and presentation modules.
3. `dp-product-new-customer-quote`
   - Official assessment workload compilation and authorized DP quote workbook generation.

The retired `dp-customer-visual-proposal` entrypoint is automatically quarantined during installation. Its reusable intake, versioning, evidence, visual, and client/internal separation capabilities have been migrated into `dp-proposal-designer`.

## Stability improvements

- Added machine-readable intake schemas and deterministic builders.
- Added fixed reusable value modules so stable content is not regenerated on every request.
- Added output contracts for annual, DP, mixed, and quote deliverables.
- Added explicit route ownership and mixed-product rules.
- Added installation backup and retired-skill quarantine.
- Added working-tree secret scanning and public response-field filtering.
- Added six automated regression tests, including post-install artifact generation.

## Quote contract

The DP quote skill calls the private authorized backend when `QUOTE_API_BASE` and `QUOTE_API_KEY` are configured. It exposes only approved client-facing fields.

The current backend regression guarantees `final_price`. `original_price` and `discount_rate` remain pending unless the backend returns them; the skill does not reverse-engineer internal pricing.

## Release boundary

The current working tree and export package exclude credentials, customer files, and internal paid materials. Existing remote Git history may still contain files from older commits and must be cleaned separately before the repository can be declared history-safe for public release.

