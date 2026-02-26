# JG agents — index (Expert tier)

## Pipeline agents

| Agent | Model | Tier | Role | Reads | Writes |
|-------|-------|------|------|-------|--------|
| **jg-planner** | gemini-3.1-pro | -- | Orchestrator; classifies complexity, routes to tiers | All artifacts (read-only), issue | state.yaml |
| **jg-subplanner** | gpt-5.1-codex-max | Standard | Decompose issue into ordered plan | Issue body | plan.json |
| **jg-subplanner-high** | gpt-5.1-codex-max | High | Decompose with dependency graphs and risk analysis | Issue body | plan.json |
| **jg-worker-fast** | gemini-3-flash | Fast | Single-file edits; escalates if exceeds scope | plan.json | worker-result.json |
| **jg-worker** | gpt-5.3-codex | Standard | Multi-file implementation | plan.json, debug-diagnosis.json | worker-result.json |
| **jg-worker-high** | gpt-5.1-codex-max | High | Complex implementation with risk assessment | plan.json, debug-diagnosis.json | worker-result.json |
| **jg-tester-fast** | gemini-3-flash | Fast | Phase 1 only (lint, typecheck, unit tests) | (runs commands) | test-result.json |
| **jg-tester** | gemini-3-flash | Standard | Phase 1 + Phase 2 verification | (runs commands) | test-result.json |
| **jg-reviewer-fast** | gemini-3-flash | Fast | Scope check and lint-level review | plan.json | review-result.json |
| **jg-reviewer** | gemini-3.1-pro | Standard | Quality gate for scope, correctness, conventions | plan.json, worker-result.json | review-result.json |
| **jg-reviewer-high** | gemini-3.1-pro | High | Deep review with architecture and security analysis | plan.json, worker-result.json | review-result.json |
| **jg-debugger** | claude-4.6-sonnet | Standard | Classify and diagnose failures | test-result.json, plan.json | debug-diagnosis.json |
| **jg-debugger-high** | claude-opus-4.6 | High | Multi-causal analysis, cross-module tracing | test-result.json, plan.json | debug-diagnosis.json |
| **jg-git** | gemini-3-flash | -- | Branch, commit, PR (no merge) | (git state) | git-result.json |
| **jg-benchmarker** | gemini-3-flash | -- | Cost/performance evaluation | Benchmark sources | Snapshot files |
| **team-linter** | gemini-3-flash | -- | Runs project linter and writes lint result | plan.json, worker-result.json | lint-result.json |

## Tier routing

| Complexity | Subplanner | Worker | Tester | Reviewer | Debugger |
|-----------|------------|--------|--------|----------|----------|
| Trivial | (skip) | jg-worker-fast | jg-tester-fast | jg-reviewer-fast | (skip) |
| Standard | jg-subplanner | jg-worker | jg-tester | jg-reviewer | jg-debugger |
| Complex | jg-subplanner-high | jg-worker-high | jg-tester | jg-reviewer-high | jg-debugger-high |

## Pipeline order

1. **jg-planner** — Classifies complexity, selects tier, orchestrates pipeline
2. **jg-subplanner[-high]** — Writes `plan.json`
3. **jg-worker[-fast|-high]** — Implements; writes `worker-result.json`
3.5. **team-linter** *(optional)* — After worker; writes `lint-result.json`. On FAIL -> planner re-dispatches worker
4. **jg-tester[-fast]** — Verifies; writes `test-result.json`. On FAIL -> debugger
5. **jg-debugger[-high]** — Diagnoses; writes `debug-diagnosis.json`. Planner re-routes
6. **jg-reviewer[-fast|-high]** — Reviews; writes `review-result.json`. On FAIL -> planner
7. **jg-git** — Ships; writes `git-result.json`
