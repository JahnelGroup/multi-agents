# Agent Registry

All agents across Foundation, Practitioner, and Expert tiers. Foundation uses 3 agents for learning; Practitioner adds the full pipeline; Expert adds tiered variants for complexity-based routing.

## Full Agent Table

| Agent | Model | Tier(s) | Role | Reads | Writes |
|-------|-------|---------|------|-------|--------|
| **jg-planner** | gemini-3.1-pro | — | Orchestrator; classifies complexity, routes pipeline and failures | All artifacts (read-only), issue | state.yaml (optional) |
| **jg-subplanner** | gpt-5.1-codex-max | Standard | Decompose issue → ordered plan | Issue body/comments | plan.json |
| **jg-subplanner-high** | gpt-5.1-codex-max | High | Decompose with dependency graphs and risk analysis | Issue body | plan.json |
| **jg-worker-fast** | gemini-3-flash | Fast | Single-file edits; escalates if exceeds scope | plan.json | worker-result.json |
| **jg-worker** | gpt-5.3-codex | Standard | Implement and test per plan | plan.json, debug-diagnosis.json | worker-result.json |
| **jg-worker-high** | gpt-5.1-codex-max | High | Complex implementation with risk assessment | plan.json, debug-diagnosis.json | worker-result.json |
| **jg-tester-fast** | gemini-3-flash | Fast | Phase 1 only (lint, typecheck, unit tests) | (runs commands) | test-result.json |
| **jg-tester** | gemini-3-flash | Standard | Phase 1 + Phase 2 verification | (runs commands) | test-result.json |
| **jg-reviewer-fast** | gemini-3-flash | Fast | Scope check and lint-level review | plan.json | review-result.json |
| **jg-reviewer** | gemini-3.1-pro | Standard | Quality gate; scope and slop | plan.json, worker-result.json | review-result.json |
| **jg-reviewer-high** | gemini-3.1-pro | High | Deep review with architecture and security analysis | plan.json, worker-result.json | review-result.json |
| **jg-debugger** | claude-4.6-sonnet | Standard | Classify and diagnose failures | test-result.json, plan.json | debug-diagnosis.json |
| **jg-debugger-high** | claude-opus-4.6 | High | Multi-causal analysis, cross-module tracing | test-result.json, plan.json | debug-diagnosis.json |
| **jg-git** | gemini-3-flash | — | Branch, commit, PR (no merge) | (git state) | git-result.json |
| **jg-benchmarker** | gemini-3-flash | — | Pull benchmarks; evaluate cost/performance; recommend models per agent | Benchmark sources, snapshot schema | benchmarks/snapshots |
| **team-linter** | gemini-3-flash | — | Runs project linter and writes lint result | plan.json, worker-result.json | lint-result.json |

**jg-benchmarker** is a support agent (on-demand), not a pipeline stage. **team-linter** is project-specific (add via tutorial or copy from sandbox).

## Tier Routing Matrix

| Complexity | Subplanner | Worker | Tester | Reviewer | Debugger |
|-----------|------------|--------|--------|----------|----------|
| Trivial | (skip) | jg-worker-fast | jg-tester-fast | jg-reviewer-fast | (skip) |
| Standard | jg-subplanner | jg-worker | jg-tester | jg-reviewer | jg-debugger |
| Complex | jg-subplanner-high | jg-worker-high | jg-tester | jg-reviewer-high | jg-debugger-high |

## Pipeline Execution Order

1. **jg-planner** — Entry point. Classifies complexity; invokes subplanner (or gives worker direct scope for trivial).
2. **jg-subplanner[-high]** — Writes `plan.json` (affected_files, steps, acceptance_mapping).
3. **jg-worker[-fast|-high]** — Implements; writes `worker-result.json`.
3.5. **team-linter** *(optional)* — After worker; writes `lint-result.json`. On FAIL → planner re-dispatches worker.
4. **jg-tester[-fast]** — Runs CI + integration; writes `test-result.json`. On FAIL → planner invokes **jg-debugger**.
5. **jg-debugger[-high]** — Writes `debug-diagnosis.json` (classification: fix_target | plan_defect | escalate). Planner re-dispatches to worker or subplanner or escalates.
6. **jg-reviewer[-fast|-high]** — Only after tester PASS. Writes `review-result.json`. On FAIL → back to planner.
7. **jg-git** — Only after reviewer PASS. Writes `git-result.json`; optionally archives `.pipeline/<issue-id>` to `.pipeline/completed/<issue-id>`.

## Subagent Types (Cursor)

When wiring to Cursor subagents, map by role. For Expert tier routing, use the tier-specific variant that matches the classified complexity.

| Role | Standard | Fast (Trivial) | High (Complex) |
|------|----------|----------------|----------------|
| planner | jg-planner | -- | -- |
| subplanner | jg-subplanner | (skip) | jg-subplanner-high |
| worker | jg-worker | jg-worker-fast | jg-worker-high |
| tester | jg-tester | jg-tester-fast | jg-tester |
| reviewer | jg-reviewer | jg-reviewer-fast | jg-reviewer-high |
| debugger | jg-debugger | (skip) | jg-debugger-high |
| git | jg-git | -- | -- |
| benchmarker | jg-benchmarker (support; invoke on-demand) | -- | -- |
| linter | team-linter (project-specific) | -- | -- |
