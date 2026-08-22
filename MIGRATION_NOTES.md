# DP Customer Visual Skill Migration

The former `dp-customer-visual-proposal` entrypoint is intentionally retired to prevent routing competition.

| Former capability | New owner | Implementation |
|---|---|---|
| Client-facing DP visual proposal | `dp-proposal-designer` | D01 contract + deterministic HTML renderer |
| Official course research | `dp-proposal-designer` | `references/official_evidence.md` |
| Intake completeness | `dp-proposal-designer` | canonical schema + validator |
| Version status | `dp-proposal-designer` | required `version_status` field and v4 gate |
| Fixed product value/process/team copy | `dp-proposal-designer` | `dp_fixed_value_modules.json` |
| Quote presentation | `dp-product-new-customer-quote` | sealed API + Q01/Q02 contracts |
| WeChat follow-up | `dp-proposal-designer` | conditional `sales_followup.md` |
| Broad product map and objection library | Not migrated | outside the three-skill product boundary |
| Customer-specific demo outputs/internal memo | Not migrated | examples are not runtime rules |

The installer quarantines the retired skill when found so it cannot compete with `dp-proposal-designer`.
