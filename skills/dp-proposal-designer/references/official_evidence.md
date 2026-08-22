# DP Official Evidence Contract

Read only when programme/module facts must be researched or verified.

Use the shared verified URL registry at `../jizhi-academic-year-plan-proposal/assets/data/official_source_registry.json` when the complete package is installed. The user instruction date determines the preferred calendar year. If that year's official information is unavailable, use the latest official university information and emit a year-mismatch warning. Every fact needs a source URL, source year and verification date.

## Source Priority

1. Official programme page.
2. Official module/course catalogue.
3. Official handbook/specification PDF.
4. Official assessment/regulation page.
5. Official academic calendar.

## Required Fields

- school, programme, degree level and target academic year;
- module code/title, credits, required/elective and teaching period;
- assessment component, weight, word count/duration and DDL when published;
- source title, source year and URL;
- confidence and missing-material note.

Official facts, customer-supplied facts and estimates must be separate. Never present a representative pathway as a confirmed module list. Never invent a weight, DDL, word count or rubric.

For quote preparation, produce one assessment component per row and hand the resulting table to `dp-product-new-customer-quote`.
