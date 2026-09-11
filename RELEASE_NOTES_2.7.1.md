# Release Notes 2.7.1

## Planning Quote Display Correction

- Planning quote sheets now show only the current package match result instead of printing the full standard quick-reference catalog by default.
- Standard quotes must display the matched package row with original price, approved saving/discount and final package price.
- Custom quotes must display course rows and a separate component calculation table. Components show original price, discount and final price, and are counted once by default unless the user explicitly requests another basis.
- Mixed DP + planning quotes keep planning and DP pricing independent, then add the approved subtotals only in the final display layer.
- Unmatched package combinations must show the calculated component original total, approved discount status and final/custom price or `待内部核价`; they must not reuse another student's package price.

## Files Updated

- `skills/jizhi-academic-year-plan-proposal/references/pricing_quote_rules.md`
- `skills/jizhi-academic-year-plan-proposal/references/planning_output_taxonomy.md`
- `skills/jizhi-academic-year-plan-proposal/scripts/build_planning_proposal.py`
- `README.md`
- `PACKAGE_CONTENTS.md`
- `VERSION`
