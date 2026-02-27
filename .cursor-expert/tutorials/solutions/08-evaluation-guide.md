# Agent Evaluation -- Solution Guide

This exercise is analytical and involves rubric design. Key evaluation criteria:

## Plan Quality Rubric (5+ criteria required)

Strong rubrics include:
1. **Acceptance criteria coverage** -- do steps map to all ACs?
2. **Step ordering** -- are dependencies respected?
3. **File scope accuracy** -- do `affected_files` and steps agree?
4. **Step granularity** -- not too vague, not too prescriptive?
5. **Risk identification** -- are assumptions and blockers flagged?

Each criterion needs a 4-point scoring scale (1=poor, 2=acceptable, 3=good, 4=excellent) with specific guidance for each level.

## Plan Evaluations

- NOTIF-001: No plan expected (trivial, skip). Explain why.
- NOTIF-002: Score each criterion. Typical weaknesses: file scope inconsistencies, missing risk notes.
- NOTIF-003: Score each criterion. Typically scores higher due to high-tier subplanner producing better plans with risk analysis.

## Review Quality Rubric (4+ criteria required)

Strong rubrics include:
1. **Finding relevance** -- are blockers actually important?
2. **Completeness** -- did the review catch visible issues?
3. **False positive rate** -- were any findings incorrect?
4. **Actionability** -- can the worker fix without clarification?

## Improvement Recommendations (2-3 required)

Each recommendation should identify:
- The pattern observed in scores
- A specific change to agent instructions, rules, or pipeline structure
- How to measure whether the change worked

Strong recommendations target systematic gaps (e.g., "subplanner should self-check file scope consistency before writing plan.json") rather than one-off issues.
