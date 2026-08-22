# 2.2.1

- 安装时创建隔离的 `~/.codex/jizhi-runtime/venv`，不修改系统 Python。
- 自动安装 Excel/PDF 必要依赖，并真实生成 XLSX/PDF 完成安装自检。
- 优先复用 Chrome/Edge；缺少浏览器时才安装 Playwright Chromium。
- Excel/PDF 脚本发现系统依赖缺失时，自动切换到隔离运行时。
- 修复虚拟环境 Python 符号链接被错误解析为系统 Python 的问题。
