# Package Contents

## Runtime Skills

- `skills/jizhi-academic-year-plan-proposal/`
  - `SKILL.md`: annual-planning entrypoint
  - `references/output_contracts.md`: fixed T00/T01/T02/T03/T04/T05 output structures
  - `references/planning_output_taxonomy.md`: academic-planning output families and the UCL-style customer-facing visual master
  - `references/client_support_proposal.md`: flexible student/family-facing customer proposal structure and tone rules
  - `references/service_packages.yaml`: sole standard-hour source
  - `references/service_logic.md`: course classification and execution rules
  - `references/pricing_quote_rules.md`: standard/custom/mixed planning quote logic, package-match display and component calculation rules
  - `assets/schemas/intake.schema.json`: canonical input contract
  - `assets/schemas/client_support_proposal.schema.json`: client-support proposal input contract
  - `assets/templates/planning_fixed_modules.json`: fixed value copy
  - `assets/templates/template_contracts.json`: fixed planning template registry
  - `assets/data/official_source_registry.json`: verified official URL cache
  - `scripts/build_planning_proposal.py`: deterministic HTML renderer
  - `scripts/build_client_support_proposal.py`: branded customer-proposal HTML renderer
  - `scripts/export_pdf.py`: verified HTML-to-PDF exporter
  - `scripts/preflight_pdf.py`: shared mandatory page/font/evidence/client-boundary/render gate for all PDF contracts
  - `scripts/build_planning_quote.py`: private pricing add-on interface
  - `scripts/update_source_registry.py`: official URL cache updater
  - `templates/fixed_cases/`: annual, public-sector, quote, Excel, and mixed visual references
- `skills/dp-proposal-designer/`
  - `SKILL.md`: DP-proposal entrypoint
  - `references/output_contracts.md`: D01/D02/D03 structures
  - `assets/templates/dp_fixed_value_modules.json`: sole fixed-value copy source
  - `scripts/validate_intake.py`: intake gate
  - `scripts/build_dp_proposal.py`: stable six-module HTML renderer
  - `scripts/export_pdf.py`: verified HTML-to-PDF exporter using the shared PDF preflight
  - `assets/templates/template_contracts.json`: fixed DP template registry
  - `assets/schemas/intake.schema.json`: canonical DP input contract
  - `templates/fixed_cases/`: generic pure-DP visual reference only
- `skills/dp-product-new-customer-quote/`
  - `SKILL.md`: DP-quote entrypoint
  - `references/output_contracts.md`: Q01/Q02 structures
  - `scripts/quote_dp_api.py`: authorized sealed quote client
  - `scripts/build_quote_workbook.py`: Assessment validation, input fingerprint, warnings and five-sheet XLSX output
  - `scripts/preflight_workbook.py`: fixed T04 sheet/header/style gate

## Package Tools

- `requirements-runtime.txt`: isolated Excel/PDF runtime dependencies
- `scripts/bootstrap_runtime.sh`: automatic runtime detection, installation and self-check
- `scripts/runtime_self_check.py`: real XLSX/PDF generation gate
- `config/skill_boundaries.json`: sole package-level ownership registry
- `scripts/route_request.py`: route regression and diagnostic helper; not a Codex runtime hook
- `install.sh`: installs exactly three skills and backs up existing versions
- `scripts/audit_boundaries.py`: checks boundaries, contracts, duplicates, and embedded quote keys
- `scripts/run_tests.sh`: fixed route, renderer, workbook, installer and audit regressions
- `scripts/quote_dp_api.py`: backward-compatible quote entrypoint
- `VERSION`: package version

Generic example files provide layout evidence only. Customer-named cases and paid pricing documents are kept in the separate `jizhi-planning-pricing-private` installation package and are not part of the public repository.
