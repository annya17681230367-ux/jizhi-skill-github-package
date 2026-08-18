# 包内容清单

## 顶层文件

- `README.md`: 包简介与快速安装。
- `USAGE_MANUAL.md`: 实用手册，说明每个 skill 能做什么。
- `GITHUB_UPLOAD_GUIDE.md`: GitHub 上传、公开/私有注意事项、安装方式。
- `.env.example`: 报价环境变量模板，不含真实接口地址和密钥。
- `.gitignore`: 避免上传 `.env`、缓存和压缩包。
- `install.sh`: 一键安装所有 skills 到 `~/.codex/skills`。
- `scripts/setup_quote_env.sh`: 管理员本机写入报价环境变量。
- `scripts/self_check_quote_api.sh`: 管理员本机报价通道自检。
- `scripts/quote_dp_api.py`: 管理员本机统一调用DP报价接口，只输出密封报价结果。

## Skills

### `skills/jizhi-academic-year-plan-proposal`

用于：

- 学业规划方案
- 全年/单学期陪跑方案
- AI智慧学习系统方案
- 学业规划报价单
- 对公精简方案
- Excel课程考核整理表
- DP + 陪跑混合边界方案

关键引用：

- `references/scenario_routing.md`
- `references/pricing_quote_rules.md`
- `references/fixed_template_cases.md`
- `references/brand_visual_spec.md`
- `references/service_logic.md`
- `templates/fixed_cases/`: 已确认的固定PDF/Excel/DOCX案例模板。
- 追加可用方案案例：UCL GHS DP安心包+考试陪跑、香港大学MAPPE对公服务匹配、悉尼大学商管DP+陪跑服务价值方案。

### `skills/dp-proposal-designer`

用于：

- DP安心包方案
- DP卓越安心包方案
- 毕业无忧方案
- 60+/65+/Distinction目标管理
- 纯DP服务方案
- DP报价规则入口

关键引用：

- `references/dp_proposal_patterns.md`
- `references/dp_pricing_rules.md`
- `references/fixed_dp_template_cases.md`
- `references/brand_visual_guidelines.md`
- `templates/fixed_cases/`: 纯DP方案和Assessment整理固定案例模板。
- 追加混合DP案例：UCL GHS、悉尼大学商管。

### `skills/dp-product-new-customer-quote`

用于：

- 课程Assessment整理
- 作业量换算
- 在授权环境中调用报价通道
- 输出最终DP报价
- 密封内部价格公式

需要：

- 管理员私下配置的 `QUOTE_API_BASE`
- 管理员私下配置的 `QUOTE_API_KEY`
- `openpyxl`
