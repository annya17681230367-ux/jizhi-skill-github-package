# 2.3.0

- Strictly separates clean client proposals from internal audit artifacts.
- Moves sources, warnings, version/contract IDs, quote traces and review status to `.internal.html/.internal.json` only.
- Restores contract-specific layouts for the six confirmed cases instead of one generic long document.
- Adds print-specific grid and page-role rules to prevent sparse mobile layouts in PDF.
- Keeps planning quote logic private and DP final pricing behind the authorized quote service.
- Adds regression checks that reject internal-text leakage into client artifacts.
