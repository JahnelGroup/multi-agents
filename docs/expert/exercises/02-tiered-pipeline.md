# Exercise 02: Tiered Pipeline

## Objective

Act as the planner and run 3 NOTIF scenarios through the pipeline, routing each to the correct tier of subagents.

!!! warning "Tiered Routing Required"
    This exercise **must** use the correct tiered subagent_types. Trivial issues use `jg-worker-fast`, `jg-tester-fast`, `jg-reviewer-fast`. Standard issues use `jg-subplanner`, `jg-worker`, `jg-tester`, `jg-reviewer`. Complex issues use `jg-subplanner-high`, `jg-worker-high`, `jg-reviewer-high`. The grader verifies tier routing.

!!! note "Required Reading"
    - [Expert walkthrough scenario](../walkthrough/scenario.md) -- the 3 NOTIF issues
    - [Expert walkthrough routing log](../walkthrough/routing-log.md) -- reference routing decisions
    - [Agent Registry](../../reference/agents.md) -- tier routing table
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- Agent definitions with `subagent_type` for dispatching tiered agents
    - [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- End-to-end feature development with agents
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- How the `jg-pipeline-artifact-io` skill guides artifact I/O during pipeline execution

=== "Cursor"
    In Cursor, use `subagent_type` to dispatch tiered agents. The artifact structure (plan.json, worker-result.json, etc.) and `tier_used` tracking are identical across environments.

=== "Claude Code"
    In Claude Code, tiered routing maps to model selection per stage. Instead of `subagent_type="jg-worker-fast"`, you would prompt a faster/cheaper model directly. The artifact structure (plan.json, worker-result.json, etc.) and `tier_used` tracking are identical.

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
3. **Delegate to `jg-worker-fast`**: implement `sandbox/src/notifications/types.ts` (TypeScript interfaces) and `sandbox/docs/api/notifications.md` (API doc). Write `worker-result.json` with `tier_used: "fast"` and `"produced_by": "jg-worker-fast"`.
4. **Delegate to `jg-tester-fast`**: Phase 1 only (lint, typecheck). Write `test-result.json` with `tier_used: "fast"`.
5. **Delegate to `jg-reviewer-fast`**: scope check. Write `review-result.json` with `tier_used: "fast"`.
6. **Delegate to `jg-git`**: branch, commit. Write `git-result.json`.

### NOTIF-002 (Standard tier)
1. Create `sandbox/.pipeline/NOTIF-002/`
2. **Delegate to `jg-subplanner`**: write `plan.json`.
3. **Delegate to `jg-worker`**: implement service and tests. Write `worker-result.json` with `tier_used: "standard"` and `"produced_by": "jg-worker"`.
4. **Delegate to `jg-tester`**: Phase 1 + Phase 2. Write `test-result.json` with `tier_used: "standard"`.
5. **Delegate to `jg-reviewer`**: full review. Write `review-result.json` with `tier_used: "standard"`.
6. **Delegate to `jg-git`**: branch, commit. Write `git-result.json`.

### NOTIF-003 (High tier)
1. Create `sandbox/.pipeline/NOTIF-003/`
2. **Delegate to `jg-subplanner-high`**: write `plan.json` with `risk_notes`.
3. **Delegate to `jg-worker-high`**: implement WebSocket handler, rate limiter, notification pusher, and tests. Write `worker-result.json` with `tier_used: "high"` and `"produced_by": "jg-worker-high"`.
4. **Delegate to `jg-tester`**: Phase 1 + Phase 2. Write `test-result.json`.
5. **Delegate to `jg-reviewer-high`**: architecture and security review. Write `review-result.json` with `tier_used: "high"`.
6. **Delegate to `jg-git`**: branch, commit. Write `git-result.json`.

## Required Schema Fields

Every `worker-result.json` must include ALL of these keys (even for trivial tasks):
- `status` (string): "completed", "failed", or "escalate"
- `files_changed` (array): list of files modified
- `blockers` (array): empty array `[]` if none
- `summary` (string): description of work done

Do NOT omit `blockers` or `summary` -- the schema validator will reject the artifact.

!!! success "Validation"
    ```bash
    python3 .cursor-expert/tutorials/verify.py --exercise 02
    ```

    Checks: all 15 artifacts exist (5 per issue), pass Expert schema.py, tier_used values correct per issue, NOTIF-001 has no plan.json, worker-result.json `produced_by` matches expected agent per tier.

??? question "Reflection"
    - How did you decide which tier to route each issue to?
    - What if NOTIF-001 turned out to need tests? Would you reclassify?
    - Compare the total artifacts produced vs a single-tier approach. What's the overhead vs benefit?
