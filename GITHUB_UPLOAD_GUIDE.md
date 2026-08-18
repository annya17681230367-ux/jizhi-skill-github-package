# GitHub 上传说明

## 推荐仓库类型

优先使用私有仓库；如果需要给同事公开分享，必须使用公开协作版。

原因：

- 包内包含品牌素材。
- 原始工作包可能包含品牌素材、内部报价资料或付费接口信息。
- DP报价接口地址、API Key、价目表、内部规则均不能公开。

## 如果必须公开仓库

公开前请确认：

```bash
grep -R "QUOTE_API_BASE=\"http" .
grep -R "QUOTE_API_KEY=\"[A-Za-z0-9]" .
find . -path "*assets/pricing*" -print
```

以上命令不应出现真实接口、真实密钥或内部报价资料。

## 初始化并上传

```bash
cd jizhi-skill-github-package_20260818
git init
git add .
git commit -m "Add Jizhi academic planning and DP skills"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## 他人安装

方式一：clone后安装

```bash
git clone <your-github-repo-url>
cd jizhi-skill-github-package_20260818
./install.sh
```

方式二：用 Codex skill-installer 从 GitHub 安装单个 skill

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/jizhi-academic-year-plan-proposal \
  --path skills/dp-proposal-designer \
  --path skills/dp-product-new-customer-quote
```

## 报价配置

普通同事不需要配置报价接口。需要最终DP报价时，把课程、Assessment、作业量和目标分发给管理员统一报价。

只有管理员机器需要配置报价环境变量：

```bash
cp .env.example .env
open .env
./scripts/setup_quote_env.sh
./scripts/self_check_quote_api.sh
```

不要提交 `.env`，也不要在群聊或公开文档里发送真实接口地址、Key、价目表或付费规则。

## 上传前检查

```bash
bash -n install.sh
bash -n scripts/setup_quote_env.sh
bash -n scripts/self_check_quote_api.sh
find . -name ".DS_Store" -o -name "*.inspect.ndjson" -o -name ".env"
grep -R "YOUR_REAL_API_KEY" . || true
```

## 当前修复点

- 海报/IP形象禁止蒙版、遮罩、覆盖层。
- DP报价使用 `dp-product-new-customer-quote` + 授权报价通道。
- DP报价不再混用学业规划陪跑报价逻辑。
- 混合方案先分开 DP 和陪跑报价，再汇总。
- 没有最终价格时继续做报价-ready表格，不编价格。
