# JG agents — index

| Agent | Model | Role | Reads | Writes |
|-------|--------|------|--------|--------|
| **jg-planner** | gemini-3.1-pro | Orchestrator; routes pipeline and failures | All artifacts (read-only), issue | state.yaml (optional) |
| **jg-subplanner** | gpt-5.1-codex-max | Decompose issue → ordered plan | Issue body/comments | plan.json |
| **jg-worker** | gpt-5.3-codex | Implement and test per plan | plan.json, debug-diagnosis.json | worker-result.json |
| **jg-tester** | gemini-3-flash | Phase 1 + Phase 2 verification | (runs CI commands) | test-result.json |
| **jg-reviewer** | gemini-3.1-pro | Quality gate; scope and slop | plan.json, worker-result.json | review-result.json |
| **jg-debugger** | claude-4.6-sonnet | Classify and diagnose failures | test-result.json, plan.json | debug-diagnosis.json |
| **jg-git** | gemini-3-flash | Branch, commit, PR (no merge) | (git state) | git-result.json |
| **jg-benchmarker** | gemini-3-flash | Pull benchmarks; evaluate cost/performance; recommend models per agent | Benchmark sources, snapshot schema | benchmarks/snapshots (project path) |
| **team-linter** | gemini-3-flash | Runs project linter and writes lint result | plan.json, worker-result.json | lint-result.json |

**jg-benchmarker** is a support agent (on-demand), not a pipeline stage.
**team-linter** is a project-specific agent (add via tutorial exercise or copy from sandbox).

## Pipeline order

1. **jg-planner** — Entry point. Classifies complexity; invokes subplanner (or gives worker direct scope for trivial).
2. **jg-subplanner** — Writes `plan.json` (affected_files, steps, acceptance_mapping).
3. **jg-worker** — Implements; writes `worker-result.json`.
3.5. **team-linter** *(optional)* — After worker; writes `lint-result.json`. On FAIL → planner re-dispatches worker.
4. **jg-tester** — Runs CI + integration; writes `test-result.json`. On FAIL → planner invokes **jg-debugger**.
5. **jg-debugger** — Writes `debug-diagnosis.json` (classification: fix_target | plan_defect | escalate). Planner re-dispatches to worker or subplanner or escalates.
6. **jg-reviewer** — Only after tester PASS. Writes `review-result.json`. On FAIL → back to planner.
7. **jg-git** — Only after reviewer PASS. Writes `git-result.json`; optionally archives `.pipeline/<issue-id>` to `.pipeline/completed/<issue-id>`.

## Subagent types (Cursor)

When wiring to Cursor subagents, map by role:

- `planner` → jg-planner
- `subplanner` → jg-subplanner
- `worker` → jg-worker
- `tester` → jg-tester
- `reviewer` → jg-reviewer
- `debugger` → jg-debugger
- `git` → jg-git
- `benchmarker` → jg-benchmarker (support; invoke on-demand for model assignment review)
- `linter` → team-linter (project-specific; add when your project has a linter)

Project-specific agent files (e.g. in `.cursor/agents/`) can be copies of these with different `name` and `model` if you want to keep jg- as a reference bundle.
