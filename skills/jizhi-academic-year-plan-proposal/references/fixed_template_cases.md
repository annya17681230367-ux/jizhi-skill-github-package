# Fixed Template Cases

Use this reference whenever the user asks for 固定模板、案例模板、按模板、产出一致、上传GitHub稳定产出, or when generating one of the known proposal/quote/table formats.

## Non-Negotiable Goal

The output should match the confirmed template family, module order, boundary rules, and file type. Do not freely invent a new structure when a fixed template applies.

## Bundled Template Assets

The confirmed case files live in:

`templates/fixed_cases/`

Key files:

- `固定模板01_标准年度学业规划方案.pdf`
- `固定模板02_对公精简服务匹配方案.pdf`
- `固定模板03_独立报价单.pdf`
- `固定模板04_Excel课程考核与报价整理表.xlsx`
- `固定模板04_Excel课程考核与报价整理表.pdf`
- `固定模板05_DP加陪跑混合边界方案.pdf`
- `固定模板06_纯DP服务方案设计.pdf`
- `UCL_GHS_大二全年DP安心包与考试陪跑方案_2026-27.pdf`
- `香港大学MAPPE硕士全年学业规划服务匹配方案_对公版.pdf`
- `悉尼大学商业管理大一学业规划陪跑DP服务方案_已删考核节点表.pdf`
- `极致学业规划Skill已确认版本案例.pdf`
- `极致学业规划Skill模板案例说明.docx`
- Assessment examples:
  - `悉尼大学政治本科三门课考核内容总表.xlsx`
  - `悉尼大学政治学大三S2_DP全包作业_Assessment整理.xlsx`

When the user requests a PDF/Excel matching a fixed case, reuse the relevant file as the visual/content template and follow the module list below.

## Template Routing

### A. 标准年度学业规划方案

Use for:
- 全年学业规划.
- 大一/硕士全年陪跑.
- 学业管家方案.
- 家长/学生完整客户方案.

Default output:
- First: structured text draft.
- After confirmation: HTML + PDF.
- Quote sheet is separate unless explicitly merged.

Fixed modules:
1. 学生与项目摘要.
2. 个人学业画像.
3. 问题诊断与定位.
4. 目标差距分析.
5. 课程优先级.
6. 阶段行动建议.
7. 学业风险清单.
8. 课程分类与课时配置.
9. 学期/全年阶段时间轴.
10. 每周执行闭环.
11. AI智慧学习系统安排.
12. 每日/每周/每月服务.
13. 预期效果.
14. 待补材料与官方来源.

### B. 对公精简服务匹配方案

Use for:
- 对公版.
- 精简版.
- 1-2页服务价值方案.
- 用户要求不要logo、不要价格、不要版本字样.
- 硕士全年服务匹配、课程考核+服务价值说明.

Default output:
- 1-2 page PDF or concise HTML/PDF.
- No price.
- No heavy sales narrative.

Fixed modules:
1. 学生/课程背景摘要.
2. 精简课程考核地图.
3. 服务匹配: DP / 陪跑 / 专业课 / AI智慧学习系统.
4. 每日、每周、每月服务内容.
5. 预期效果.
6. 待确认材料.

Do not keep long, crowded assessment-node tables if the user asks for a client-ready concise version. Convert to summary rows/cards.

Confirmed usable case:
- `香港大学MAPPE硕士全年学业规划服务匹配方案_对公版.pdf`

MAPPE-style fixed pattern:
- Use restrained B2B wording.
- Focus on course assessment + support match, not promotional language.
- Keep service value visible: what academic planning does, what teachers do, what AI智慧学习系统 does.
- Keep quote separate unless explicitly requested.

### C. 纯课程考核 + 服务匹配表

Use for:
- 只整理Assessment.
- 课程考核与服务匹配.
- 官网信息整理.
- 客户/内部快速确认表.

Default output:
- Excel first when table is requested.
- PDF table only when user asks for visual PDF.

Required fields:
- 课程代码.
- 课程名称.
- 评估项目.
- 占比.
- 个人/小组.
- 截止日期.
- 形式/时长.
- 具体要求.
- 提供服务.
- 来源/备注.

Rules:
- Each assessment row must identify the course.
- Translate official English task descriptions into Chinese client-readable wording.
- Do not fabricate DDL, word count, or rubric. Mark unknown items as `待Moodle/Assessment Brief/Rubric确认`.

### D. 独立报价单

Use for:
- 报价单.
- 内部报价.
- 客户报价.
- 原价/折后价.

Default output:
- Separate PDF/Excel.
- Not merged into proposal unless explicitly requested.

Required modules:
1. 对应方案信息.
2. 服务范围.
3. 课程分类.
4. 每门课课时/组件.
5. 原价.
6. 折扣逻辑.
7. 折后价.
8. 付款/有效期 note if supplied.
9. 二次核算检查.

Rules:
- 学业规划/陪跑报价 uses `pricing_quote_rules.md`.
- DP报价 uses DP pricing rules and authorized quote channel.
- Never expose API keys, endpoint URLs, bottom line, margin, or internal formulas in client-facing output.

### E. 标准套餐全年陪跑方案

Use for:
- User asks for全年/学期陪跑 but does not provide custom hours.

Rules:
- Default to standard package.
- 重点课程 and 非重点课程 classification decides hours.
- Do not create custom hour splits unless user explicitly asks for 定制方案/定制课时 or gives exact hours.

### F. 定制方案

Use only when:
- User explicitly says 定制方案 / 定制课时.
- User gives exact professional/陪跑/规划执行 hours per course.

Rules:
- Use user-provided hours.
- Clearly label custom logic.
- Quote separately and show assumptions.

### G. DP + 陪跑混合边界方案

Use for:
- Same student has DP assignment support and separate exam/course-understanding support.
- User says DP + 陪跑, mixed, 混合方案.
- Full-year DP安心包 plus exam/course tutoring support.
- Single-term business-management plans where written/group tasks go DP and exam preparation goes陪跑/专业课.

Fixed modules:
1. 产品分流: which courses/tasks are DP vs 陪跑.
2. DP service scope: writing/report/presentation/project/capstone.
3. 陪跑 service scope: exam, concepts, weekly learning execution, specialist teaching.
4. AI智慧学习系统 role.
5. Separate quote logic blocks if quote is requested.

Rules:
- DP and陪跑 must be separated.
- DP price cannot use陪跑 standard package prices.
- 陪跑 price cannot use DP service language.
- If the user asks for a client-facing plan, avoid showing dense raw assessment-node tables; summarize course risks and service match instead.
- The expected effect should say DP handles assignment quality/60+ target management, while陪跑/专业课 teaches course understanding and exam readiness. Do not promise guaranteed grades.

Confirmed usable cases:
- `UCL_GHS_大二全年DP安心包与考试陪跑方案_2026-27.pdf`
- `悉尼大学商业管理大一学业规划陪跑DP服务方案_已删考核节点表.pdf`

UCL GHS-style fixed pattern:
- Use when a year-long plan combines DP安心包 with exam/course tutoring.
- Show annual service period, course coverage, DP scope, exam support scope, and risk-management rhythm.
- Keep DP and exam/陪跑 responsibilities separate throughout the proposal.

Sydney Commerce-style fixed pattern:
- Use when the user explicitly wants customer-facing service value and has asked to remove/avoid overly long assessment-node tables.
- Use compact assessment summaries and service cards instead of a full DDL wall.
- Include daily/weekly/monthly service actions and AI智慧学习系统 usage.
- Do not include logo or quote if the user asks for a clean client/public version.

### H. Excel模板整理版

Use for:
- User provides or asks for Excel template.
- 用户说“按照这个表格/模板整理”.

Default output:
- `.xlsx`.

Rules:
- Follow the field boundary of `固定模板04_Excel课程考核与报价整理表.xlsx`.
- Keep course code and Chinese/English course names visible.
- Source/备注 should be separate enough for review.
- Formula/total rows must be checked before delivery.

## Universal Template Rules

- Default first response is text draft unless user explicitly asks for final PDF/Excel directly.
- Proposal and quote are separate by default.
- Official source evidence is mandatory for course facts.
- Unknown official details must remain pending, not invented.
- Every standard planning proposal must include the six confirmed planning items:
  - 个人学业画像.
  - 问题诊断与定位.
  - 目标差距分析.
  - 课程优先级.
  - 阶段行动建议.
  - 学业风险清单.
- DP and陪跑 boundaries must stay separate.
- Before final delivery, check layout, math, quote boundary, sources, and hidden internal content.
