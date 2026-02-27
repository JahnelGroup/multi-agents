# Tiered Pipeline -- Solution Guide

This exercise is hands-on (delegation to subagents). The key points for a correct solution:

## Routing decisions

| Issue | Complexity | Tier | Subplanner? | Tester Phase |
|-------|-----------|------|------------|-------------|
| NOTIF-001 | Trivial | Fast | Skip | Phase 1 only |
| NOTIF-002 | Standard | Standard | Yes | Phase 1 + 2 |
| NOTIF-003 | Complex | High | Yes (high) | Phase 1 + 2 |

## Artifact requirements per issue

### NOTIF-001 (5 artifacts, no plan.json)
- `worker-result.json` with `tier_used: "fast"`, `produced_by: "jg-worker-fast"`
- `test-result.json` with `tier_used: "fast"`
- `review-result.json` with `tier_used: "fast"`
- `git-result.json`
- No `plan.json` -- trivial tasks skip planning

### NOTIF-002 (6 artifacts)
- `plan.json` with `produced_by: "jg-subplanner"`
- `worker-result.json` with `tier_used: "standard"`, `produced_by: "jg-worker"`
- `test-result.json` with `tier_used: "standard"`
- `review-result.json` with `tier_used: "standard"`
- `git-result.json`

### NOTIF-003 (6 artifacts)
- `plan.json` with `risk_notes`, `produced_by: "jg-subplanner-high"`
- `worker-result.json` with `tier_used: "high"`, `produced_by: "jg-worker-high"`
- `test-result.json`
- `review-result.json` with `tier_used: "high"`
- `git-result.json`

## Common mistakes

- Including `plan.json` for NOTIF-001 (trivial tasks skip planning)
- Using wrong `produced_by` values (must match the tiered agent name)
- Omitting `blockers` or `summary` from `worker-result.json` (schema requires all keys)
- Using `tier_used: "standard"` for NOTIF-003 (must be `"high"`)
