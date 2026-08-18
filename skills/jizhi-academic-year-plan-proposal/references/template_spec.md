# Template Spec

Use this reference when the user says “按照这个模板”, “参考 neon-hamster 页面”, “做全年方案”, or “年度课业规划方案”.

## Draft vs Final
- First draft: structured Markdown/text only, unless the user explicitly asks for final PDF/design rendering.
- Confirmed final: branded HTML/PDF after content is approved.
- Proposal and quote are separate by default. Do not include any amount, discount, payment, or quote content in the proposal.

## Fixed Section Order
1. **Hero**
   - Brand mark/name.
   - Label: `学校 + 学年/年级 + 方案类型`.
   - H1: `Program + 年级 + 全年学业规划方案`.
   - Intro: start date, coverage period, scope, and overall service logic.

2. **KPI Cards**
   - Total recommended hours.
   - Specialist teaching hours.
   - Planning/execution support hours.
   - Number of required/covered courses.
   - If hours are provisional, mark `暂估`.
   - Unless定制方案 is explicitly requested, KPI hours must come from the standard package classification: 重点课程 or 非重点课程.

3. **Core Judgment**
   - One paragraph explaining the real risk.
   - Must go beyond “课程很多”.
   - Mention assessment types, language/academic ability, DDL concurrency, oral/viva/exam risks, and why student-side understanding matters.
   - Include hour split visualization.

4. **Course Classification**
   - Identify重点课程 and non重点 courses.
   - Explain why the priority exists.
   - State allocation principle.
   - State that actual order adjusts by DDL, assessments, and weakness signals.

5. **Student Background Diagnosis**
   - Three panels:
     - 专业适配
     - 能力风险
     - 服务策略

6. **Course Cards**
   For every course/module:
   - cluster
   - priority: `重点/非重点 · 风险等级`
   - Chinese title
   - English title/code
   - assessment focus
   - risk judgment
   - strategy
   - hour split: specialist + execution/support + total
   - For default proposals, hour split must use standard package hours. Do not create custom per-course hours unless the user explicitly requests定制方案.

7. **Term/Calendar Stage Arrangement**
   Use a phase table:
   - phase name
   - date range
   - academic period/weeks
   - hours
   - stage focus

8. **Concrete Annual Path**
   Use 6-8 steps, each with:
   - step number
   - date/time range
   - title
   - action
   - output

9. **Weekly Execution Loop**
   Use 5 steps:
   - 周一 资料同步
   - 周二/三 专业课深度讲解
   - 周四 AI智慧学习系统练习与检测
   - 周五/六 规划执行课复盘
   - 周日 周报与下周计划

10. **DDL and Assessment Nodes**
   - Timeline of important academic dates.
   - Official assessment components: name, weight, type, week/DDL, word count/duration where available.
   - Official source links or source file names.
   - Pending items: Canvas/Moodle/Assessment Brief/Rubric details not yet available.
   - Student cooperation list.

11. **AI智慧学习系统 Path**
   Seven nodes:
   - 课程知识库
   - 学生画像
   - 学
   - 练
   - 用
   - 造
   - 人工介入

12. **Course-Specific AI智慧学习系统 Usage**
   For each high-risk or representative course:
   - course name
   - how AI智慧学习系统 is used
   - what is checked

13. **Service Delivery Modules**
   Six cards:
   - 课程资料整理
   - AI智慧学习系统
   - 每周学习反馈
   - 家长月度反馈
   - Assessment节点管理
   - 出分与Feedback复盘

14. **Resource Configuration**
   Four cards:
   - 专业课老师
   - 规划执行课老师/陪跑课老师
   - 学习管理老师
   - AI智慧学习系统

15. **Expected Outcome**
   One paragraph summarizing what the student should gain by each period.
   Must include service value and expected effect, without guaranteed grade/pass wording.

16. **Footer**
   Mention sources and assumptions.
   Always include: `正式执行以学生入学后的Programme Handbook、Moodle和Assessment Brief为准。`

## Writing Density
This template is information-dense. Do not turn it into a landing page. Charts, tables, and cards should carry real decision content.

## Naming Defaults
Default to:
- `学业规划`
- `年度学业规划方案`
- `规划执行课`
- `AI智慧学习系统`

Use `陪跑` only when the user explicitly asks or when the plan is for an internal product that uses that package name.
