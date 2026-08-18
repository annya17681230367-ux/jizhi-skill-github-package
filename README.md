# 极致学业规划 / DP 方案 Skill 包

这个仓库用于把当前已稳定的 Codex skills 分享给其他同事安装使用，核心目标是让产出结构更稳定、报价逻辑更明确、视觉规则更一致。

## 包含的 Skills

### 1. `jizhi-academic-year-plan-proposal`

用于生成学业规划、全年/单学期课业规划、学业管家方案、AI智慧学习系统方案、陪跑课/专业课配置、报价单等。

稳定产出重点：

- 标准年度学业规划方案
- 对公精简服务匹配方案
- 独立报价单
- Excel课程考核整理表
- DP + 陪跑混合边界方案
- 品牌/IP视觉规范
- 固定案例模板复现
- 可用方案案例复现：UCL GHS DP安心包+考试陪跑、香港大学MAPPE对公版、悉尼大学商管DP+陪跑服务价值版

### 2. `dp-proposal-designer`

用于生成 DP安心包、DP卓越安心包、毕业无忧、60+/65+/Distinction目标管理方案。

稳定产出重点：

- 纯DP服务方案
- 官方课程结构与Assessment表
- 目标分风险管理
- DP服务内容与质量控制
- 团队配置与流程
- DP报价规则入口

### 3. `dp-product-new-customer-quote`

用于整理官方课程Assessment、计算作业量，并在授权环境中生成DP最终报价。

稳定产出重点：

- 单sheet Excel报价交付
- 官方课程与作业量整理
- 密封报价：只展示最终价，不展示内部公式

## 快速安装

```bash
git clone <your-repo-url>
cd <repo-folder>
./install.sh
```

安装后，重新打开 Codex 或开启下一轮对话，让 skills 生效。

## DP 报价配置

普通同事不需要配置报价接口。DP报价建议由管理员或指定报价人员统一执行，避免价格体系和付费接口外泄。

如管理员需要在本机启用报价能力，可复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env`，填入私下提供的报价接口地址和密钥。

也可以写入本机 shell：

```bash
./scripts/setup_quote_env.sh
```

配置完成后自检：

```bash
./scripts/self_check_quote_api.sh
```

管理员也可以直接用统一脚本请求报价：

```bash
python3 scripts/quote_dp_api.py --payload-json '{"school":"UCL","program":"Economics","degree_level":"UG","target_year":"2026/27","scope":"课程作业","total_words":32000}'
```

输出只展示报价结果，不展示 Key 或内部公式。

## 安全说明

- 不要把真实 `QUOTE_API_BASE` 或 `QUOTE_API_KEY` 上传到公开仓库。
- 不要在公开文档、截图或群聊里暴露报价接口地址、Key、底价、利润或内部公式。
- `.env` 已经加入 `.gitignore`。
- GitHub 包内只保留 `.env.example`。

## 主要修复

1. IP形象不允许使用蒙版、遮罩、覆盖层或被卡片压住。
2. DP报价增加独立规则和授权报价入口，不再混用学业规划陪跑报价逻辑。
3. 混合方案必须拆成 `DP报价逻辑` 与 `学业规划陪跑报价逻辑` 两块。
4. 缺少最终价格时继续生成范围和内部报价草稿，标记 `待价格文件核对` 或 `待报价API恢复后计算`。
5. 固定模板案例已进入 skill，安装后可按模板稳定生成相同结构的方案、报价单和Excel表。
