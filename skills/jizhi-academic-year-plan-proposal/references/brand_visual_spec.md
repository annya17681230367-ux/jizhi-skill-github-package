# Brand Visual Spec

Use this whenever generating a branded 极致AI学业规划 HTML/PDF proposal or quote sheet.

## Required Brand Assets

Resolve assets relative to the skill folder:

- Full logo: `assets/brand/full-logo.jpg`
- IP images:
  - `assets/ip/study-dashboard.jpg`
  - `assets/ip/research-files.jpg`
  - `assets/ip/report-scroll.jpg`
  - `assets/ip/portrait-star.jpg`
  - `assets/ip/standing.jpg`
  - `assets/ip/graduation.jpg`
  - `assets/ip/cheer.jpg`
  - `assets/ip/pass-test.jpg`
  - `assets/ip/checklist.jpg`

## Header Rule

- The upper-left page/header area must use the full horizontal logo, not the cropped square `AI` mark, unless the user explicitly asks for a compact logo.
- Keep the logo on a white or very pale blue background so the grey Chinese logotype remains readable.
- Recommended logo CSS:

```css
.brand-logo {
  width: 260px;
  max-width: 42%;
  height: auto;
  object-fit: contain;
  display: block;
}
```

For A4 PDFs, use about `180-240px` wide in normal section headers and `260-340px` wide on the cover/hero page.

## Palette

Base the proposal on the IP colors:

- Deep navy: `#102a63`
- Logo blue: `#1463ff`
- Cyan: `#10d6c8`
- IP purple: `#7d67f2`
- Soft blue background: `#f4f8ff`
- Panel blue: `#edf7ff`
- Accent yellow: `#ffd84d`, used sparingly for tags or totals only

Avoid beige, brown, heavy dark slate, or single-hue blue-only pages. The page should feel blue-cyan with a small purple IP accent.

## Background And Page Feel

- Default document background: `#f4f8ff` or a very light blue/cyan wash.
- Panels remain white with thin blue borders and light shadows.
- Use cyan/purple accents to match the IP, but keep text areas quiet and readable.
- Do not place dark IP images behind body text.
- Do not overuse decorative gradients; one header gradient and a few accent tags are enough.

## IP Image Placement

Use IP images to fill whitespace and support meaning:

- Cover/hero: `study-dashboard.jpg` or `research-files.jpg` as a right-side visual block or faint background crop.
- Student profile / diagnosis: `research-files.jpg`.
- Course planning / report delivery: `report-scroll.jpg` or `checklist.jpg`.
- Assessment / pass target: `pass-test.jpg`.
- Graduation / annual outcome: `graduation.jpg` or `cheer.jpg`.
- AI智慧学习系统: `study-dashboard.jpg`.
- Light filler: `portrait-star.jpg` or `standing.jpg` placed at bottom-right or side whitespace.

Rules:

- IP images should not compete with core tables or course cards.
- Do not apply masks, gradient masks, clipping masks, blur overlays, dark overlays, or semi-transparent panels on top of IP characters. The character cannot look like it is covered by a veil.
- When an IP character is used as a foreground/supporting visual, use full opacity and `object-fit: contain`; keep the full character visible.
- Background fillers may use low opacity (`0.10-0.18`), but they still must not be masked or hidden behind text blocks. Prefer placing them in empty side/bottom whitespace.
- Crop with `object-fit: cover` only for abstract background screenshots or non-character scenes. Use `object-fit: contain` for all character-focused IP images.
- On A4 print pages, keep IP visuals inside page boundaries and avoid covering text.
- Before final export, visually check that no IP image is overlapped by cards, text, tables, gradient panels, or page-edge clipping.

## Suggested Components

```css
.brand-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 36px;
  background: linear-gradient(135deg, #f8fbff, #eef9ff);
}

.ip-watermark {
  position: absolute;
  right: 26px;
  bottom: 24px;
  width: 190px;
  opacity: .14;
  pointer-events: none;
  object-fit: contain;
}

.ip-panel {
  border: 1px solid #cfe7ff;
  background: linear-gradient(180deg, #ffffff, #f4fbff);
  border-radius: 10px;
  overflow: hidden;
}
```

## Hard No-Mask Rule

For all posters, proposal covers, service-flow graphics, and PDF pages:

- Never use CSS `mask`, `clip-path`, `mix-blend-mode`, heavy opacity overlays, or gradient covers on IP character images.
- Never put a semi-transparent white/blue/purple rectangle over the IP character.
- If the layout needs a soft decoration, move the IP to an empty corner and reduce the image opacity directly; do not cover it with another layer.
- If the IP looks unclear after export, remove the IP or place it in a clean visual block instead of masking it.

## Quote Sheet

- Quote sheets should also use the full horizontal logo in the upper-left.
- Use a blue-cyan header and a dark navy-to-cyan total block.
- Always show original price, discount/savings logic, and final discounted price. If no discount is specified, show `暂无折扣` and make the final discounted price equal the original price.
- IP usage on quote sheets should be minimal: one faint side/bottom visual only if it does not distract from numbers.
