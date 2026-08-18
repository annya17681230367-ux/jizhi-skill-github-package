# HTML Style Spec

Use this when creating the actual HTML proposal.

## Visual Direction
Match the referenced template:
- consulting-style, information-dense, clean.
- blue/cyan/purple palette aligned with the 极致AI logo and IP illustration set.
- white panels with subtle borders and shadows.
- 8px border radius for professional cards.
- use the bundled 极致AI full logo and IP illustrations when creating branded HTML/PDF proposals.
- desktop-first single page, responsive enough for mobile.

## Suggested CSS Tokens
- ink: `#121826`
- muted: `#5b6472`
- line: `#d8dee8`
- blue: `#1463ff`
- cyan: `#10d6c8`
- purple: `#7d67f2`
- navy: `#102a63`
- gold: `#ffd84d`
- bg: `#f4f8ff`
- panel: `#ffffff`
- soft: `#edf7ff`

## Layout Components
Use:
- branded header with the full horizontal 极致AI logo in the upper-left.
- KPI card grid.
- two-column split panels.
- three-card diagnosis grid.
- two-column course module grid.
- phase table with four columns.
- horizontal scroll annual pathway.
- five-column weekly loop.
- dark AI智慧学习系统 section.
- course usage table.
- service card grid.
- resource role grid.
- subtle IP image filler in page whitespace when it improves balance.

## HTML Rules
- Create a standalone `.html` file when asked for a visual proposal.
- Keep all CSS in the file unless a project build system already exists.
- Use semantic sections and clear headings.
- Avoid SVG-only decorative visuals; use CSS, tables/cards, and the bundled raster logo/IP assets.
- For local HTML export, reference assets with `file://` absolute paths or copy them into the output folder.
- If exporting to PDF/PNG, render with headless Chrome and visually inspect.

## Client Readability
- Prefer short paragraphs inside cards.
- Use bold labels for `考核侧重点`, `风险判断`, `策略`.
- Do not let visual polish remove operational details.
