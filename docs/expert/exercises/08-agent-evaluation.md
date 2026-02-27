# Exercise 08: Agent Evaluation and Quality Rubrics

## Objective

Design an evaluation rubric for assessing the quality of agent outputs, then apply it to walkthrough artifacts. This moves beyond structural schema validation (does the JSON have the right fields?) to semantic quality assessment (is the plan actually good?).

!!! note "Required Reading"
    - [Expert walkthrough scenario](../walkthrough/scenario.md) -- The NOTIF scenario that produced the artifacts you will evaluate
    - [Expert walkthrough routing log](../walkthrough/routing-log.md) -- Routing decisions and tier selections
    - [Expert walkthrough cost summary](../walkthrough/cost-summary.md) -- Cost analysis from the walkthrough
    - [Reviewing and Testing Code | Cursor Learn](https://cursor.com/learn/reviewing-and-testing-code) -- Review patterns applicable to evaluating agent work
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- Understanding agent capabilities and limitations

=== "Cursor"
    Evaluation rubrics and LLM-as-a-Judge patterns work identically whether agents are invoked via Cursor subagents or Claude Code sequential prompting.

=== "Claude Code"
    Evaluation rubrics and LLM-as-a-Judge patterns are IDE-agnostic. The same rubric criteria and scoring approach work whether agents are invoked via Cursor subagents or Claude Code sequential prompting.

## Context

Schema validation catches missing fields but cannot tell you if a plan is well-structured, if step ordering makes sense, or if a review caught the right issues. In production, teams use evaluation rubrics -- structured scoring criteria that can be applied by humans or LLMs -- to measure agent output quality over time.

This technique is known as **LLM-as-a-Judge**: using a language model (or structured rubric) to evaluate the outputs of another model. It enables automated quality tracking and continuous improvement.

## Tasks

### Part 1: Design a Plan Quality Rubric

Create an evaluation rubric for `plan.json` artifacts. Your rubric must define at least 5 criteria, each with:

- **Criterion name** (e.g., "Acceptance criteria coverage")
- **What it measures** (one sentence)
- **Scoring scale**: 1 (poor), 2 (acceptable), 3 (good), 4 (excellent)
- **Scoring guidance**: What a 1, 2, 3, and 4 look like for this criterion

Suggested criteria (use at least 3 of these, add 2+ of your own):
- Acceptance criteria coverage: Do the steps map to all acceptance criteria?
- Step ordering: Are dependencies respected? Would this order work if executed literally?
- File scope accuracy: Are `affected_files` correct and complete?
- Step granularity: Are steps too broad (vague) or too narrow (micromanaging)?
- Risk identification: Does the plan flag potential issues or assumptions?

### Part 2: Apply the Rubric

Evaluate the `plan.json` artifacts from the NOTIF walkthrough. Score each plan against your rubric:

- `NOTIF-001` (trivial -- no plan expected; note why it was skipped)
- `NOTIF-002` (standard complexity)
- `NOTIF-003` (high complexity)

For each scored plan, provide:
- Per-criterion score (1-4)
- Brief justification for each score
- Overall quality verdict: Strong / Adequate / Needs Improvement

### Part 3: Design a Review Quality Rubric

Create a second rubric for `review-result.json` artifacts with at least 4 criteria. Suggested criteria:
- Finding relevance: Are blockers/concerns actually important?
- Completeness: Did the review catch issues visible in the diff?
- False positive rate: Were any findings incorrect or nitpicky-as-blockers?
- Actionability: Are findings specific enough to fix?

### Part 4: Improvement Recommendations

Based on your evaluation, write 2-3 specific recommendations for improving agent output quality. For each recommendation, explain:
- What pattern you observed in the scores
- What change to agent instructions, rules, or pipeline structure would address it
- How you would measure whether the change worked

## Output

Write to `.cursor-expert/tutorials/outputs/08-evaluation-rubrics.md` with these sections:

```markdown
## Plan Quality Rubric
(5+ criteria with scoring scales)

## Plan Evaluations
(Scored evaluations for NOTIF-002 and NOTIF-003)

## Review Quality Rubric
(4+ criteria with scoring scales)

## Improvement Recommendations
(2-3 specific, actionable recommendations)
```

!!! success "Validation"
    ```bash
    python3 .cursor-expert/tutorials/verify.py --exercise 08
    ```

    Checks: file exists with 4 sections, plan rubric has 5+ criteria, review rubric has 4+ criteria, evaluations reference NOTIF issues, recommendations section has sufficient depth.

??? question "Reflection"
    - How would you automate this evaluation so it runs after every pipeline completion?
    - What are the risks of using an LLM to evaluate another LLM's output?
    - How would evaluation rubrics differ for a healthcare application vs. an e-commerce application?
    - Could the benchmarker agent be extended to include output quality scores alongside model performance benchmarks?

??? success "Answer"
    **Plan Quality Rubric** (5+ criteria): acceptance criteria coverage, step ordering, file scope accuracy, step granularity, risk identification. Each scored 1-4 with specific guidance per level.

    **Plan Evaluations**: NOTIF-001 has no plan (trivial, correct to skip). NOTIF-002 typically scores ~2.5/4 (adequate but file scope inconsistencies and missing risk notes). NOTIF-003 typically scores ~3.7/4 (strong -- high-tier subplanner produces better risk analysis).

    **Review Quality Rubric** (4+ criteria): finding relevance, completeness, false positive rate, actionability.

    **Improvement Recommendations**: Target systematic gaps like "enforce plan self-consistency checks before writing" and "require risk_notes for standard+ plans."

    See `.cursor-expert/tutorials/solutions/08-evaluation-guide.md` in the source repo for a complete exemplar.
