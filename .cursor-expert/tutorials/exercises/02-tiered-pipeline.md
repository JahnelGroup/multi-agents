# Exercise 02: Tiered Pipeline

## Objective

Act as the planner and run 3 NOTIF scenarios through the pipeline, routing each to the correct tier of subagents.

## Required Reading

- [Expert walkthrough scenario](../../walkthrough/scenario.md) -- the 3 NOTIF issues
- [Expert walkthrough routing log](../../walkthrough/routing-log.md) -- reference routing decisions
- [Expert AGENTS.md](../../AGENTS.md) -- tier routing table

## Context

3 issues from the notification system scenario, each at a different complexity level:

| Issue | Description | Tier |
|-------|------------|------|
| NOTIF-001 | Define notification API contract | Trivial -> Fast |
| NOTIF-002 | Implement notification service | Standard |
| NOTIF-003 | Add real-time WebSocket delivery with rate limiting | Complex -> High |

## Tasks

### NOTIF-001 (Fast tier)
1. Create `sandbox/.pipeline/NOTIF-001/`
2. Skip subplanner (trivial tasks skip planning)
3. **Delegate to `jg-worker-fast`**: implement `sandbox/src/notifications/types.ts` (TypeScript interfaces) and `sandbox/docs/api/notifications.md` (API doc). Write `worker-result.json` with `tier_used: "fast"`.
4. **Delegate to `jg-tester-fast`**: Phase 1 only (lint, typecheck). Write `test-result.json` with `tier_used: "fast"`.
5. **Delegate to `jg-reviewer-fast`**: scope check. Write `review-result.json` with `tier_used: "fast"`.
6. **Delegate to `jg-git`**: branch, commit. Write `git-result.json`.

### NOTIF-002 (Standard tier)
1. Create `sandbox/.pipeline/NOTIF-002/`
2. **Delegate to `jg-subplanner`**: write `plan.json`.
3. **Delegate to `jg-worker`**: implement service and tests. Write `worker-result.json` with `tier_used: "standard"`.
4. **Delegate to `jg-tester`**: Phase 1 + Phase 2. Write `test-result.json` with `tier_used: "standard"`.
5. **Delegate to `jg-reviewer`**: full review. Write `review-result.json` with `tier_used: "standard"`.
6. **Delegate to `jg-git`**: branch, commit. Write `git-result.json`.

### NOTIF-003 (High tier)
1. Create `sandbox/.pipeline/NOTIF-003/`
2. **Delegate to `jg-subplanner-high`**: write `plan.json` with `risk_notes`.
3. **Delegate to `jg-worker-high`**: implement WebSocket handler, rate limiter, notification pusher, and tests. Write `worker-result.json` with `tier_used: "high"`.
4. **Delegate to `jg-tester`**: Phase 1 + Phase 2. Write `test-result.json`.
5. **Delegate to `jg-reviewer-high`**: architecture and security review. Write `review-result.json` with `tier_used: "high"`.
6. **Delegate to `jg-git`**: branch, commit. Write `git-result.json`.

## Validation

```bash
python3 .cursor-expert/tutorials/verify.py --exercise 02
```

Checks: all 15 artifacts exist (5 per issue), pass Expert schema.py, tier_used values correct per issue, NOTIF-001 has no plan.json.

## Reflection

- How did you decide which tier to route each issue to?
- What if NOTIF-001 turned out to need tests? Would you reclassify?
- Compare the total artifacts produced vs a single-tier approach. What's the overhead vs benefit?
