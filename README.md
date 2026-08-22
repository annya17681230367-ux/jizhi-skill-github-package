# 极致学业规划与 DP Skills

Version `2.2.0` fixes three independent product boundaries and adds executable, regression-tested generation paths.

## Three Skills

| Skill | Owns | Must not own |
|---|---|---|
| `jizhi-academic-year-plan-proposal` | 个性化学业规划报告、客户学业方案、全年/学期规划、陪跑、专业课、AI智慧学习系统及规划报价 | 纯DP方案、DP最终报价 |
| `dp-proposal-designer` | 纯DP客户方案、固定价值模块、服务流程、DP风险与执行安排 | 最终DP价格、陪跑课时价格 |
| `dp-product-new-customer-quote` | 官方Assessment工作量、密封DP报价、报价Excel | 方案叙事、年度规划、陪跑报价 |

混合产品由年度规划 skill 组织结构；DP模块由 DP 方案 skill 输出；DP价格由 DP 报价 skill 返回。三块数据不得合并计算。

## Install

```bash
git clone <repository-url>
cd jizhi-skill-github-package
./install.sh
```

安装器只安装上述三个 skill，将旧版本备份到 `~/.codex/skill-backups/`，并自动隔离已废弃的 `dp-customer-visual-proposal`、`jizhi-academic-planning-report` 和 `jizhi-essay-customer-proposal` 入口。

## Deterministic Output

1. Each request selects exactly one output contract before writing.
2. Fixed service-value copy is loaded from one asset, not rewritten per customer.
3. Official assessment facts remain dynamic and source-backed.
4. Final DP pricing is available only through the authorized quote helper.
5. Example PDFs are visual references, not runtime instructions.
6. Every proposal includes a fixed `课程与服务匹配` module and a machine-readable warning sidecar.
7. Official facts prefer the request-year source, fall back to the latest official source, and retain the source URL.

`scripts/route_request.py` is a regression-test and diagnostic helper. Actual Codex routing is controlled by the three non-overlapping `SKILL.md` descriptions.

Run the complete regression suite before release:

```bash
TEST_PYTHON=python3 scripts/run_tests.sh
```

## DP Quote Authorization

The public repository contains no credentials, endpoint URL, or private formula. Authorized users configure `QUOTE_API_BASE` and `QUOTE_API_KEY` locally, then call:

```bash
python3 scripts/quote_dp_api.py --payload-json '<payload>'
```

Or build the complete Assessment + quote workbook:

```bash
python3 skills/dp-product-new-customer-quote/scripts/build_quote_workbook.py assessment.json quote.xlsx --request-quote
```

Without authorization, the skill may prepare assessment evidence but must not invent or finalize a price.

The current quote API guarantees `final_price`. Original price and discount are displayed only when the authorized backend returns them; the public skill never reverse-engineers them.

## Planning Quote Add-on

陪跑/学业规划价格不放在公开仓库。内部人员另行安装 `jizhi-planning-pricing-private` 后，年度规划 Skill 才能通过 `build_planning_quote.py` 计算并追溯原价、折后价、输入指纹和预警。未安装时必须停止报价，不得猜价。

## Security

- Never commit `.env`, API keys, endpoint URLs, or screenshots containing credentials.
- Never expose paid formulas or raw private API responses.
- Customer-named cases and internal planning price files live outside the public repository.
- Run the boundary audit and a separate secret scan before every public push.
