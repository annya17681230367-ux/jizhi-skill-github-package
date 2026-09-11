# Release Notes 2.7.0

## Added

- Added `references/planning_output_taxonomy.md` to define the academic-planning output families and the UCL-style project-management visual master.
- Documented how standard plans, custom plans, mixed DP + planning proposals, public-sector concise plans and planning quote sheets should present their content.
- Extended the client-support proposal guidance so mixed DP + light-pacing plans use table-first course configuration, separate DP workload, exam support, calendar, responsibilities and execution-condition pages.

## Updated

- Updated `SKILL.md`, `output_contracts.md` and `README.md` to make the UCL-style customer-facing design the default for future T01/T02/T03 variants, custom plans and mixed plans.
- Kept pricing boundaries intact: planning and DP quote logic remain separate, and public materials must not expose private formulas, endpoints or trace details.

## Compatibility

- Existing fixed generators and legacy preflight gates are preserved until their implementation is migrated.
- The flexible `CLIENT_SUPPORT` route is the preferred path when the user asks for the newer, more polished customer-facing proposal style.
