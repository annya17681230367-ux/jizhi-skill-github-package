# 极致学业规划与 DP Skills

Version `2.7.0` standardizes the UCL-style project-management visual master for customer-facing academic planning outputs, including standard plans, custom plans, mixed DP + planning proposals and planning quote sheets.

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

安装器会在 `~/.codex/jizhi-runtime/` 创建隔离 Python 环境，自动检测或安装 Chromium，并实测生成 XLSX 与 PDF；不会修改系统 Python。随后安装三个 Skill、备份旧版本，并隔离已废弃入口。网络受限时也可先执行 `JIZHI_SKIP_RUNTIME_SETUP=1 ./install.sh`，但 Excel/PDF 在完成运行时配置前不可用。

## Deterministic Output

1. Each request selects exactly one output contract before writing.
2. Fixed service-value copy is loaded from one asset, not rewritten per customer.
3. Official assessment facts remain dynamic and source-backed.
4. Final DP pricing is available only through the authorized quote helper.
5. Example PDFs are visual references, not runtime instructions.
6. Every proposal includes a fixed `课程与服务匹配` module and a machine-readable warning sidecar.
7. Official facts prefer the request-year source, fall back to the latest official source, and retain the source URL.
8. Student/family-facing customer proposals use the flexible `CLIENT_SUPPORT` route when the user asks for a branded, service-focused PDF.

## Client-Support Proposal Route

For polished customer proposals, use:

```bash
python3 skills/jizhi-academic-year-plan-proposal/scripts/build_client_support_proposal.py \
  tests/fixtures/client_support_sim_dit.json \
  output/client_support.html
```

Then export the HTML to PDF with Chromium/Chrome and visually inspect the rendered pages. This route is intentionally not fixed to the old T01 exactly-three-page gate.

## Output Families And Design

Read `skills/jizhi-academic-year-plan-proposal/references/planning_output_taxonomy.md` before building or revising customer-facing planning outputs. The current default style is:

- Cover with a large blue-gradient title block, target/hour metric cards and one concise project-management judgment.
- Course/service mapping in compact tables instead of repeated course-risk cards.
- Standard plans: diagnosis, course configuration, lesson structure, timeline, AI learning system and execution responsibilities.
- Custom plans: course tiering, user-stated lesson caps, professional/pacing split and dynamic adjustment points.
- Mixed DP + planning plans: separate course configuration, DP workload, exam/professional lesson support, calendar, responsibilities and formal execution conditions.
- Quote sheets: price cards, authorized price tables and quick-reference course-count/重点非重点 combination tables when useful.

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
