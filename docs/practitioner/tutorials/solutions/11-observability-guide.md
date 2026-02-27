# Pipeline Observability -- Solution Guide

This exercise has two outputs: a `pipeline-trace.json` artifact and an observability analysis.

## pipeline-trace.json structure

A valid trace for the ISSUE-42 walkthrough must reflect the full execution timeline including the test failure and retry:

```json
{
  "issue_id": "ISSUE-42",
  "stages": [
    { "stage": "plan", "agent": "jg-subplanner", "started_at": "2026-02-20T10:00:00Z", "duration_ms": 8000, "result": "pass", "artifact": ".pipeline/ISSUE-42/plan.json" },
    { "stage": "implement", "agent": "jg-worker", "started_at": "2026-02-20T10:00:08Z", "duration_ms": 15000, "result": "pass", "artifact": ".pipeline/ISSUE-42/worker-result.json" },
    { "stage": "test", "agent": "jg-tester", "started_at": "2026-02-20T10:00:23Z", "duration_ms": 5000, "result": "fail", "artifact": ".pipeline/ISSUE-42/test-result-fail.json" },
    { "stage": "debug", "agent": "jg-debugger", "started_at": "2026-02-20T10:00:28Z", "duration_ms": 10000, "result": "pass", "artifact": ".pipeline/ISSUE-42/debug-diagnosis.json" },
    { "stage": "implement", "agent": "jg-worker", "started_at": "2026-02-20T10:00:38Z", "duration_ms": 8000, "result": "pass", "artifact": ".pipeline/ISSUE-42/worker-result.json" },
    { "stage": "test", "agent": "jg-tester", "started_at": "2026-02-20T10:00:46Z", "duration_ms": 5000, "result": "pass", "artifact": ".pipeline/ISSUE-42/test-result-pass.json" },
    { "stage": "review", "agent": "jg-reviewer", "started_at": "2026-02-20T10:00:51Z", "duration_ms": 12000, "result": "pass", "artifact": ".pipeline/ISSUE-42/review-result.json" },
    { "stage": "git", "agent": "jg-git", "started_at": "2026-02-20T10:01:03Z", "duration_ms": 3000, "result": "pass", "artifact": ".pipeline/ISSUE-42/git-result.json" }
  ],
  "total_duration_ms": 66000,
  "produced_by": "jg-planner"
}
```

Key: must include at least 6 stages, include both pass and fail results, and reflect the retry cycle.

## Observability analysis key points

### Why traces matter
- Artifacts show what was decided; traces show when, how long, and what path was taken
- A pipeline with 2 retries looks identical to a first-pass success from artifacts alone
- Traces reveal performance bottlenecks and retry patterns

### Cost visibility
- Add `input_tokens`, `output_tokens`, `model`, and `cost_usd` per stage
- Sum to `total_cost_usd` at the top level
- Enables cost-per-issue tracking and model cost optimization

### Failure debugging
- Traces show the causal chain: which stage failed, what debugger found, whether retry succeeded
- Without traces, you reconstruct this from timestamps or git history (unreliable)

### Production monitoring metrics
- Average cycle time (plan to git)
- Retry rate (% of runs with debug/retry cycles)
- Cost per issue (by tier, by complexity)
- Stage hotspots (which stages are slowest/most expensive)
- Failure classification distribution (fix_target vs plan_defect vs escalate)
