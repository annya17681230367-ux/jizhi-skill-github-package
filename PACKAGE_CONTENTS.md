# Package Contents

## Runtime Skills

- `skills/jizhi-academic-year-plan-proposal/`
  - `SKILL.md`: annual-planning entrypoint
  - `references/output_contracts.md`: T00/T01/T02/T03/T05 output structures
  - `references/service_packages.yaml`: sole standard-hour source
  - `references/service_logic.md`: course classification and execution rules
  - `assets/schemas/intake.schema.json`: canonical input contract
  - `assets/templates/planning_fixed_modules.json`: fixed value copy
  - `assets/templates/template_contracts.json`: fixed planning template registry
  - `assets/data/official_source_registry.json`: verified official URL cache
  - `scripts/build_planning_proposal.py`: deterministic HTML renderer
  - `scripts/export_pdf.py`: verified HTML-to-PDF exporter
  - `scripts/build_planning_quote.py`: private pricing add-on interface
  - `scripts/update_source_registry.py`: official URL cache updater
  - `templates/fixed_cases/`: annual, public-sector, quote, Excel, and mixed visual references
- `skills/dp-proposal-designer/`
  - `SKILL.md`: DP-proposal entrypoint
  - `references/output_contracts.md`: D01/D02/D03 structures
  - `assets/templates/dp_fixed_value_modules.json`: sole fixed-value copy source
  - `scripts/validate_intake.py`: intake gate
  - `scripts/build_dp_proposal.py`: stable six-module HTML renderer
  - `scripts/export_pdf.py`: verified HTML-to-PDF exporter
  - `assets/templates/template_contracts.json`: fixed DP template registry
  - `assets/schemas/intake.schema.json`: canonical DP input contract
  - `templates/fixed_cases/`: generic pure-DP visual reference only
- `skills/dp-product-new-customer-quote/`
  - `SKILL.md`: DP-quote entrypoint
  - `references/output_contracts.md`: Q01/Q02 structures
  - `scripts/quote_dp_api.py`: authorized sealed quote client
  - `scripts/build_quote_workbook.py`: Assessment validation, input fingerprint, warnings and five-sheet XLSX output

## Package Tools

- `config/skill_boundaries.json`: sole package-level ownership registry
- `scripts/route_request.py`: route regression and diagnostic helper; not a Codex runtime hook
- `install.sh`: installs exactly three skills and backs up existing versions
- `scripts/audit_boundaries.py`: checks boundaries, contracts, duplicates, and embedded quote keys
- `scripts/run_tests.sh`: fixed route, renderer, workbook, installer and audit regressions
- `scripts/quote_dp_api.py`: backward-compatible quote entrypoint
- `VERSION`: package version

Generic example files provide layout evidence only. Customer-named cases and paid pricing documents are kept in the separate `jizhi-planning-pricing-private` installation package and are not part of the public repository.
