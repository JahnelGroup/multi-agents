# Exercise 11: Pipeline Observability

## Objective

Understand why observability matters for multi-agent pipelines and create a `pipeline-trace.json` artifact that records what happened during a pipeline run. This is the foundation for cost analysis and debugging in production.

## Required Reading

- `.cursor/skills/jg-pipeline-artifact-io/SKILL.md` -- Directory layout including `pipeline-trace.json`
- `.cursor-practitioner/pipeline/schema.py` -- Schema showing required fields for `pipeline-trace.json`
- [Putting It Together | Cursor Learn](https://cursor.com/learn/putting-it-together) -- End-to-end workflows

> **Claude Code**: Observability concepts are IDE-agnostic. In any system, tracking which agent ran, how long it took, and what it produced is essential for debugging and cost management.

## Context

When a pipeline runs, you get the final artifacts (plan, worker-result, test-result, etc.) but not the execution timeline. Without a trace, you cannot answer:

- How long did each stage take?
- Which agent was invoked at each step?
- Were there retries or failures along the way?
- What was the total cost of the run?

A `pipeline-trace.json` artifact fills this gap by recording the execution timeline in structured form.

## Tasks

### Part 1: Create a pipeline trace

Create `sandbox/.pipeline/ISSUE-42/pipeline-trace.json` that reconstructs the execution timeline for the Issue-42 walkthrough. Use the existing artifacts in `sandbox/.pipeline/ISSUE-42/` to inform your trace.

Required fields (validated by `schema.py`):

- `issue_id`: `"ISSUE-42"`
- `stages`: Array of stage records, each with:
  - `stage`: Stage name (e.g., `"plan"`, `"implement"`, `"test"`, `"debug"`, `"review"`, `"git"`)
  - `agent`: Agent that executed the stage (e.g., `"jg-subplanner"`)
  - `started_at`: ISO 8601 timestamp
  - `duration_ms`: Duration in milliseconds
  - `result`: `"pass"` or `"fail"`
  - `artifact`: Path to the output artifact
- `total_duration_ms`: Sum of all stage durations
- `produced_by`: `"jg-planner"`

The trace should reflect the Issue-42 narrative: plan, implement, test (fail), debug, implement (retry), test (pass), review, git.

### Part 2: Write an observability analysis

Write to `tutorials/outputs/11-observability-analysis.md` explaining:

1. **Why traces matter** -- What questions can you answer with a trace that you cannot answer from artifacts alone?
2. **Cost visibility** -- How would you extend the trace to track token usage and model costs per stage?
3. **Failure debugging** -- How does the trace help when a pipeline produces unexpected results?
4. **Production monitoring** -- What metrics would you derive from traces across many pipeline runs? (e.g., average cycle time, retry rate, cost per issue)

## Output

1. `sandbox/.pipeline/ISSUE-42/pipeline-trace.json` -- Valid trace artifact
2. `tutorials/outputs/11-observability-analysis.md` -- Analysis with 4 sections

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 11
```

Checks: `pipeline-trace.json` exists, passes schema validation, has at least 6 stage entries, includes both pass and fail results. Analysis file exists with 4 sections, each with sufficient depth.
