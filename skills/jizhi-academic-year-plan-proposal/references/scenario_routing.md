# Scenario Routing: DP方案 vs 学业规划陪跑方案

Use this reference before generating a proposal when the user request could mean either:

- DP/安心包/卓越安心包/Distinction Pass proposal
- 学业规划/全年陪跑/学业管家/AI智慧学习系统 proposal

## Hard Boundary

Do not mix the two systems.

- DP方案 and 学业规划陪跑方案 can share course research, risk diagnosis, visual polish, and PDF export habits.
- They must not share quote formulas, package names, service promises, or client-facing product positioning.

## Route To DP Proposal Logic

Use DP logic when the user mentions any of:

- `DP`
- `Distinction Pass`
- `安心包`
- `卓越安心包`
- `毕业无忧`
- `65+方案`
- `60+稳分`
- `Distinction方案`
- `保分方案`
- `学年包升级DP`
- `DP托管`

DP proposal positioning:

- Sells managed academic outcomes and long-cycle quality control, not ordinary陪跑.
- Product names include `DP安心包`, `DP卓越安心包`, or `毕业无忧`.
- Client-facing text frames score targets as risk management, such as `围绕65+目标做风险管理`.
- Quote page appears only when requested or when enough DP price direction exists.
- Never expose internal quote formulas, bottom line, margin, or negotiation room.

For DP work, use the installed `dp-proposal-designer` skill and its references:

- `/Users/a005/.codex/skills/dp-proposal-designer/SKILL.md`
- `/Users/a005/.codex/skills/dp-proposal-designer/references/dp_proposal_patterns.md`
- `/Users/a005/.codex/skills/dp-proposal-designer/references/brand_visual_guidelines.md`
- `/Users/a005/.codex/skills/dp-proposal-designer/references/dp_pricing_rules.md` when DP价格、报价、报价单、费用、原价、折后价 are requested.

DP visual identity:

- Use Distinction Pass logo/assets from `dp-proposal-designer/assets/`.
- Palette: brand blue `#005CFF`, DiDi Mint `#3BDBBD`, light cyan `#65C8D0`, periwinkle/violet accents.

## Route To 学业规划陪跑 Logic

Use 学业规划陪跑 logic when the user mentions any of:

- `学业规划`
- `全年陪跑`
- `课业陪跑`
- `学业管家`
- `AI智慧学习系统`
- `专业课`
- `规划执行课`
- `陪跑课`
- `标准套餐`
- `定制陪跑`
- `课程规划`
- `报价单` attached to a confirmed学业规划方案

学业规划陪跑 positioning:

- Sells course planning, weekly execution, professional teaching, AI智慧学习系统, DDL/risk tracking, and parent-visible feedback.
- Default方案 uses标准套餐 unless the user explicitly requests定制方案.
- Quote follows `pricing_quote_rules.md`, not DP quote logic.

## If Both Appear

If a user asks for both DP and陪跑 in one request:

1. Create separate sections or separate deliverables:
   - `DP方案`
   - `学业规划陪跑方案`
2. Ask for confirmation before quoting if product boundary changes the price.
3. Label quote logic separately:
   - `DP报价逻辑`
   - `学业规划陪跑报价逻辑`

Never calculate one final total by blending DP and陪跑 formulas unless the user explicitly provides a combined commercial package and confirms the components.

If the user asks for a mixed quote, do not stall:

- Calculate or draft the DP section using DP pricing rules.
- Calculate or draft the陪跑 section using 学业规划陪跑 pricing rules.
- Mark missing prices as `待价格文件核对`.
- Show a combined total only after both subtotals are visible and reconcilable.
