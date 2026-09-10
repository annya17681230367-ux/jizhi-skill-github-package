# Release Notes 2.6.0

## Added

- Added `CLIENT_SUPPORT`, a flexible branded customer-proposal route for student/family-facing academic support plans.
- Added `references/client_support_proposal.md` for tone, structure, course-risk matching, lesson mix and brand/IP rules.
- Added `scripts/build_client_support_proposal.py`, which renders a branded A4 HTML proposal from a structured JSON intake.
- Added `assets/schemas/client_support_proposal.schema.json` and a SIM DIT client-support fixture.
- Added regression coverage for customer-proposal markers and forbidden client-facing copy.

## Notes

- Fixed T00/T01/T02/T03/T05 contracts remain unchanged.
- `CLIENT_SUPPORT` is intentionally not bound to the old T01 exactly-three-page gate.
- Pricing remains excluded unless explicitly requested and authorized through the proper pricing route.
