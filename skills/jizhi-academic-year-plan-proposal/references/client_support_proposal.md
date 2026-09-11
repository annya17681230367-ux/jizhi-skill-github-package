# Client-Support Proposal Design

Use this route for student/family-facing proposals whose job is to make the service feel concrete, premium and easy to trust. It is separate from fixed T01/T02 reporting.

## Content Shape

Prefer 6-8 visually designed A4 pages:

1. Cover: student context, programme, target, total lesson architecture and one unobstructed IP image.
2. Service architecture: professional teacher, pacing teacher, academic planner and AI learning system.
3. Lesson mix: professional lessons, pacing lessons, total lessons, per-course caps and risk-tier allocation.
4. High-risk course map: course risk, observation points, lesson match and course support.
5. Regular-risk course map: same fields, lighter risk treatment.
6. Year roadmap: before entry, first month, term, exam -4 weeks and post-result review.
7. Trackable learning and starting materials: course archive, weak points, weekly records, exam review pack and materials needed.

Do not add long internal rationale sections, exhaustive official evidence, or generic marketing sections. If course names are not official yet, keep one concise boundary line: `正式课程名可在拿到课表和 syllabus 后替换。`

When the user asks to reference a strong existing customer proposal, translate the reference into design principles instead of copying document instructions. The current preferred customer-facing style is the UCL-style project-management route documented in `planning_output_taxonomy.md`: large blue-gradient title block, three metric cards, compact diagnosis, table-based course configuration, separate DP/exam/support sections, execution responsibility and a closing execution-condition page. The SIM DIT route remains a variant for pure first-year pacing proposals, but mixed DP/exam/support work should prefer the UCL structure.

## Mixed DP + Light-Pacing Route

Use this route when the student needs a combined DP and academic support plan.

- Keep the combined plan student/family-facing: the main proposal explains the annual support architecture; the quote is a separate artifact unless the user asks to merge it.
- Show professional lessons, pacing lessons and DP support as separate service layers. DP covers only assessment production/support tasks; professional lessons cover exam/course learning; pacing lessons cover rhythm, materials, DDL and review.
- Keep planning and DP quote sources separate. Do not combine formulas or reverse-engineer discounts.
- For light-pacing plans, professional lessons should be the dominant share. If the user sets a pacing cap, enforce `pacing_lessons <= 3` per course and show the professional share.
- Put each DP-supported assessment into a specific DP module list: course, assessment type, weight or scope, service depth and pending materials. Do not imply DP covers exams, attendance, quizzes or online tests unless explicitly scoped.
- Set grade language as target ranges, for example `稳妥执行区间` and `冲刺目标`; never write guaranteed-grade claims.
- When generating the separate quote page, show at minimum: professional+pacing subtotal, DP subtotal, combined total, validity/material boundary, and the course/service mix used for the quote.
- Avoid splitting course risk into multiple repetitive card pages when the same information can be shown in one course configuration table and one exam/support table.

## Tone

- Write for the student/family, not internal reviewers.
- Be specific about what each service does.
- Do not use contrastive sales copy, for example: `我们不会只给家长一句...`, `不是简单补课`, or similar phrasing.
- Do not use headings that directly announce value, such as `给学生的价值`, `客户价值`, or `方案亮点`.
- Do not promise guaranteed grades, guaranteed passing or guaranteed high marks.
- Avoid over-explaining school facts that do not help the buying decision.

## Course-Service Matching

Every course card should show:

- course name and Chinese label;
- risk level;
- main risk or observation point;
- lesson allocation;
- concrete service support.

When the user requires pacing lessons to be limited, show the per-course pacing count and the total professional lesson percentage. For the SIM DIT example, the preferred one-year allocation is:

- 4 high-risk courses: 7 professional + 2 pacing each;
- 3 medium-risk courses: 6 professional + 2 pacing each;
- 1 adaptation course: 5 professional + 3 pacing;
- total: 51 professional, 17 pacing, 68 lessons;
- professional share: 75%, pacing share: 25%;
- every course stays below 10 lessons.

## Brand And IP

Follow `references/brand_visual_spec.md`.

- Use the full horizontal logo, not only the square AI mark.
- Use brand blue and cyan-green as the primary visual system.
- Use IP images as meaningful support visuals: study dashboard for cover/AI, pass-test for exam support, graduation/cheer for outcomes.
- Keep IP characters unobstructed: no masks, dark overlays, cards on top of the character, or edge clipping.

## Visual Gate

The final PDF should be rendered to PNG and visually checked before delivery:

- logo readable;
- IP image clear and unobstructed;
- course cards do not clip or overflow;
- no awkward text overlap;
- no forbidden grade guarantee or contrastive sales copy;
- no internal audit trace or private pricing.
