# DP Quote API Contract

## Request

Required public payload fields:

`school | program | degree_level | target_year | scope | total_words`

Optional fields:

`package_type | target_score`

## Response

Required field: `final_price`.

Allowed client-facing fields: `package_type`, `scope`, `original_price`, `discount_rate`, `final_price`, `currency`.

As of the 2.1.0 regression test, the authorized backend returns `package_type`, `scope`, `final_price`, and `currency`, but does not return `original_price` or `discount_rate`. The public skill must show those two fields as pending rather than derive them from an undisclosed formula.

The backend must add `original_price` and `discount_rate` before original-versus-discount presentation can be treated as a complete API-backed quote.
