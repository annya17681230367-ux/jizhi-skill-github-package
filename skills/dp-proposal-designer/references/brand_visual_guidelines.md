# Brand Visual Guidelines

Use this reference when generating a visual DP proposal, PDF, HTML page, slide, or client-facing plan.

## Brand Assets

Available assets:

- `assets/distinction-pass-logo-wide.png`: primary transparent wide logo with icon + `distinction pass 极致教育`.
- `assets/distinction-pass-logo-wide-alt.png`: alternate copy of the transparent wide logo.
- `assets/distinction-pass-icon.png`: square icon extracted for small UI marks.
- `assets/brand-color-system.png`: VI page showing primary and secondary color system.
- `assets/logo-background-usage.png`: logo usage on different backgrounds.
- `assets/logo-usage-examples.png`: logo application examples.
- `assets/poster-layout-examples.png`: poster / layout rhythm examples.
- `assets/visual-application-examples-1.png` and `assets/visual-application-examples-2.png`: broader brand application examples.
- `assets/brand-texture-patterns.png`: texture / pattern references.

Do not load or embed every reference image by default. Use them only when designing the visual direction or when the user asks for brand/IP integration.

## Palette

Primary DP colors should follow the user's VI source file (`极致教育VI 低版本 (6).ai`) and the Distinction Pass logo:

- Brand blue: `#005CFF`
- DiDi Mint: `#3BDBBD` (RGB 59, 219, 189)
- Light cyan: `#65C8D0`
- Soft periwinkle: `#838BC5`
- Soft violet: `#BA9BC9`
- Logo / body grey: `#666666`
- White / off-white: `#FFFFFF`, `#F4FBFC`, `#F8FAFC`

Use blue and mint as the dominant pair. Use light cyan/periwinkle/violet only for subtle section accents, small tags, dividers, or background pattern hints. Avoid using generic dark teal as the dominant proposal color unless the user requests a dark version.

## Logo Usage

Use the wide logo on:

- Cover header.
- Footer / closing page.
- Title pages for formal PDF proposals.

Use the icon mark on:

- Small corner badges.
- Process cards.
- Section dividers.
- Browser/favicon-like local previews.

Keep enough white or dark clean space around the logo. Avoid placing it on busy photography or dense tables.

## IP / Graphic Usage

The VI file includes brand application pages, textures, posters, and small education/travel/academic icons. Use these as inspiration for:

- Light blue-cyan geometric background accents.
- Subtle pattern bands or section dividers.
- Small academic planning icons when helpful.

Do not over-decorate proposal pages. DP方案 should still feel like a premium consulting document: structured, precise, and trust-building.

## Proposal Layout Defaults

For DP proposals:

- Use a clean white or bright brand-blue/mint hero with the logo visible in the first viewport/page.
- Do not place internal edition labels such as `客户发送版`, `样例模板`, `官网检索版`, or `报价确认版` on the client cover. If a working version label is needed, keep it in the file name or internal note, not visible on the cover.
- Keep cards at 8px radius.
- Use dense tables for official course structure and assessment analysis.
- Use process cards/timelines for DP service value.
- Use one or two accent colors at a time; avoid a rainbow palette.
- Keep client-facing documents free of internal memo, quote formulas, or negotiation notes.

## Recommended CSS Tokens

```css
:root {
  --brand-blue: #005CFF;
  --brand-mint: #3BDBBD;
  --brand-cyan: #65C8D0;
  --brand-periwinkle: #838BC5;
  --brand-violet: #BA9BC9;
  --brand-grey: #666666;
  --page-bg: #F4FBFC;
}
```

Hero gradient:

```css
background: linear-gradient(120deg, #005CFF 0%, #3BDBBD 72%, #65C8D0 100%);
```
