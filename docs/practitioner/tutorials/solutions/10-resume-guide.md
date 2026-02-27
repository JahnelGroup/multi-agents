# Resume Pipeline -- Solution Guide

This exercise has two outputs: a `state.yaml` file and a resume analysis.

## state.yaml key fields

A valid `state.yaml` for the RESUME-01 scenario must include:

```yaml
issue: "Add rate limiting middleware"
issue_number: 101
status: paused
current_stage: test
acceptance_criteria:
  - description: "Rate limiting middleware rejects requests exceeding threshold"
    status: implemented
  - description: "Rate limiter returns 429 with Retry-After header"
    status: implemented
stages:
  plan:
    agent: jg-subplanner
    result: PASS
    summary: "Decomposed rate limiting into 3 steps"
  implement:
    agent: jg-worker
    result: PASS
    summary: "Implemented rate limiter middleware and tests"
retries: []
running_summary: "Pipeline paused during test stage. Plan and implementation complete. Resume by dispatching jg-tester."
```

## Resume analysis key points

### What the planner reads
- `status: paused` signals resumption, not fresh start
- `current_stage: test` tells the planner which agent to dispatch
- `stages` with completed records confirms which artifacts exist
- `acceptance_criteria` shows what's implemented but unverified

### What stages are skipped
- Plan and implement are skipped because `state.yaml` records them as completed
- Re-running them risks producing different plans that conflict with existing code

### Risks of resuming
1. Source code changed between sessions (worker-result no longer reflects disk state)
2. Stale plan due to scope change (issue updated while paused)
3. Dependency/environment drift (node_modules changed)
4. Clock/timing issues for time-sensitive features

### Mitigations
- Diff check on `files_changed` before resuming
- Re-read issue and compare acceptance criteria to state
- Verify lockfile hasn't changed
- Use deterministic time mocking in tests
