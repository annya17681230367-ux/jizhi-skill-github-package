# Three-Skill Architecture

## Root Causes Fixed

1. **Overlapping entrypoints**: legacy planning-report and customer-proposal skills competed with the annual-planning owner, while two DP proposal skills competed for pure-DP requests.
2. **Repeated rules**: package hours, pricing notes, DP value copy, and template descriptions appeared in several files and drifted independently.
3. **Examples treated as instructions**: large customer PDFs and case notes were repeatedly read even when only one output type was required.
4. **Execution outside the owner**: the DP quote helper lived at repository root, so installed skills could lose the capability.
5. **No release gate**: duplicate templates, extra skill directories, and embedded credentials were not blocked automatically.

## Stable Design

- Exactly three public skills. `config/skill_boundaries.json` is the package-level ownership registry.
- Each skill has one concise `SKILL.md` and one `references/output_contracts.md`.
- Fixed content has a single source per owner: planning modules in `planning_fixed_modules.json`; DP value copy in `dp_fixed_value_modules.json`; template boundaries in each owner's `template_contracts.json`.
- Customer facts, official evidence, course risks, dates, and task mapping remain dynamic.
- Every proposal contract includes `课程与服务匹配`; workload basis and source state remain visible for review.
- Official URLs are retained in `official_source_registry.json`; request-year official evidence is preferred, then the latest official evidence.
- HTML-to-PDF export is executable and page-count checked rather than recreated ad hoc.
- DP quote execution ships inside the DP quote skill and fails closed without local authorization.
- Planning pricing is a separate private add-on. The public repository contains only its fail-closed interface.
- Ambiguity, model-estimated workload, unsupported package combinations and missing authoritative facts emit the fixed warning prefix and sidecar.

## Upgrade Rule

1. Decide which owner changes.
2. Update only that skill's contract, fixed asset, or script.
3. Do not copy the change into sibling skills.
4. Run `scripts/audit_boundaries.py` and deterministic sample tests.
5. Increase `VERSION` only after all three installed-skill validations pass.

This design stabilizes structure and fixed wording. Dynamic official facts can still change when university sources change; they must be re-verified rather than cached as permanent copy.
