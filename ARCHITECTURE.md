# Three-Skill Architecture

## Root Causes Fixed

1. **Overlapping entrypoints**: two DP proposal skills competed for the same request, while the annual skill also contained pure-DP templates.
2. **Repeated rules**: package hours, pricing notes, DP value copy, and template descriptions appeared in several files and drifted independently.
3. **Examples treated as instructions**: large customer PDFs and case notes were repeatedly read even when only one output type was required.
4. **Execution outside the owner**: the DP quote helper lived at repository root, so installed skills could lose the capability.
5. **No release gate**: duplicate templates, extra skill directories, and embedded credentials were not blocked automatically.

## Stable Design

- Exactly three public skills. `config/skill_boundaries.json` is the package-level ownership registry.
- Each skill has one concise `SKILL.md` and one `references/output_contracts.md`.
- Fixed content has a single source: planning hours in `service_packages.yaml`; DP value copy in `dp_fixed_value_modules.json`.
- Customer facts, official evidence, course risks, dates, and task mapping remain dynamic.
- Example files are visual references and are opened only after an output contract is selected.
- DP quote execution ships inside the DP quote skill and fails closed without local authorization.

## Upgrade Rule

1. Decide which owner changes.
2. Update only that skill's contract, fixed asset, or script.
3. Do not copy the change into sibling skills.
4. Run `scripts/audit_boundaries.py` and deterministic sample tests.
5. Increase `VERSION` only after all three installed-skill validations pass.

This design stabilizes structure and fixed wording. Dynamic official facts can still change when university sources change; they must be re-verified rather than cached as permanent copy.
