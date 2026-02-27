---
name: execute-training-course
overview: Act as a developer-in-training to complete all 25 exercises across Foundation (6), Practitioner (11), and Expert (8) tiers. Read each exercise, delegate to multi-agent subagents as required, generate all outputs, and run the grader to prove the course is fully functional.
todos:
  - id: reset
    content: Run make reset to wipe previous outputs and start clean
    status: pending
  - id: foundation-execution
    content: Complete Foundation Exercises (01-06) and pass phase-2 validation
    status: pending
  - id: practitioner-execution
    content: Complete Practitioner Exercises (01-11) via subagent delegation and pass phase-3 validation
    status: pending
  - id: expert-execution
    content: Complete Expert Exercises (01-08) via tiered subagent routing and pass phase-4 validation
    status: pending
  - id: final-grader
    content: Run ./test-all.sh to confirm all 25 exercises pass
    status: pending
isProject: false
---

# Testing

An agent acts as a student-in-training: complete every exercise, delegate to subagents where required, generate all outputs, then run the grader to verify the course works end-to-end.

## How to use

**Grade your work** (human or agent -- verifies outputs exist and are correct):

```bash
./test-all.sh              # grade all phases
./test-all.sh --phase 2    # grade Foundation only
./test-all.sh --phase 3    # grade Practitioner only
./test-all.sh --phase 4    # grade Expert only
```

**Run the full course as an agent** (integration test -- proves the course works):

```bash
make reset                 # wipe all outputs, restore sandbox to base state
```

Then ask your agent to execute the phases below. The agent resets, completes all 25 exercises (delegating to subagents where required), and runs the grader. If the grader passes, the course is fully functional.

**Reset only** (wipe outputs without grading -- also reinstalls sandbox deps):

```bash
make reset
```

This wipes `.pipeline/`, all `tutorials/outputs/`, and `sandbox/.pipeline/`.

---

## Delegation Requirements (CRITICAL)

The following rules are mandatory. Violating them means the exercise FAILS.

1. **Use the Task tool with the correct `subagent_type`**. Exercises that say "delegate to jg-subplanner" mean: call the Task tool with `subagent_type: "jg-subplanner"`. The subagent must do the actual work inside its Task invocation.
2. **Do NOT bypass delegation**. If a `subagent_type` is unavailable or the Task call fails, the exercise FAILS. Do NOT write pipeline artifacts manually as a fallback. Never write `"produced_by": "jg-subplanner"` (or any agent name) into an artifact that was not actually produced by that subagent.
3. **Do NOT delegate entire tiers to generalPurpose agents**. The top-level agent must dispatch each delegation exercise individually using the specified `subagent_type`. A `generalPurpose` sub-agent cannot further dispatch to `jg-subplanner`, `jg-worker`, etc.
4. **Subagents write their own artifacts**. Each subagent creates its output files directly. The top-level agent does not post-process or rewrite subagent artifacts.
5. **The grader cross-references artifacts against disk state**. `produced_by` is checked, but it is not sufficient. The grader also verifies that `files_changed` entries exist as real files, `affected_files` reference plausible paths, and review findings point to actual source files.

---

## Delegation Integrity

The grader does **not** trust self-reported metadata alone. `produced_by` is a necessary field, but the grader also cross-references artifacts against the actual state of the filesystem:

| Verification layer | What it catches |
|--------------------|-----------------|
| `produced_by` field | Agent that should have produced the artifact wrote its name |
| `files_changed` cross-reference | Every file listed in `worker-result.json` must exist on disk |
| `affected_files` plausibility | Plan paths must be plausible sandbox paths (e.g. start with `src/`) |
| Review findings file check | Reviewer findings that reference a `file` must point to a real file |
| Git branch existence | `git-result.json` branch must exist in the sandbox git history |
| `npm test` | Code written by the worker must compile and pass tests |
| `check.py` stage-gate | Pipeline invariants (ordering, scope, tier routing) validated |
| Agent name cross-reference | Benchmark report agent names must correspond to actual `.md` agent files |
| Fast-tier escalation artifact | Escalation exercises must include the initial fast-tier result |

When running the course as an agent, the agent **must** use the Task tool with the correct `subagent_type` for each delegation exercise. Writing artifacts manually and faking `produced_by` will be caught by the cross-reference checks above. See **Delegation Requirements** above.

---

## Cursor & Claude Code Documentation

Each tutorial exercise links to the relevant official documentation. These are the key reference pages used throughout the course:

**Cursor Learn** (concept-driven guides):
- [Agents](https://cursor.com/learn/agents) -- What agents are and how they work
- [Customizing Agents](https://cursor.com/learn/customizing-agents) -- Creating and configuring custom agents
- [Working with Agents](https://cursor.com/learn/working-with-agents) -- Practical interaction patterns
- [Developing Features](https://cursor.com/learn/creating-features) -- End-to-end feature development
- [Finding and Fixing Bugs](https://cursor.com/learn/finding-and-fixing-bugs) -- Debug workflows
- [Reviewing and Testing Code](https://cursor.com/learn/reviewing-and-testing-code) -- Review and test patterns
- [Putting It Together](https://cursor.com/learn/putting-it-together) -- Combined workflows

**Cursor Docs** (reference):
- [Custom Agents](https://docs.cursor.com/agent/custom-agents) -- Agent `.md` frontmatter, AGENTS.md, `subagent_type` mapping
- [Rules](https://docs.cursor.com/context/rules) -- `.mdc` rule files, frontmatter, activation
- [Agent Skills](https://docs.cursor.com/context/skills) -- `SKILL.md` format, discovery, activation

**Claude Code** (equivalent concepts -- not implemented in this repo):
- Claude Code uses `CLAUDE.md` (analogous to `.cursor/rules/`), `.claude/skills/SKILL.md` (identical format to Cursor skills), and sequential prompting with model selection (analogous to `subagent_type` dispatch). The exercises and artifacts in this repo are designed to be IDE-portable.

---

## Prerequisites

- **Python** 3.10+ (for `schema.py`, `check.py`, and each tier's `verify.py`)
- **Node.js** 20+ and **npm** (for the sandbox project)
- **git** (for branch/commit checks in Practitioner exercise 05)
- **Cursor** with an agent capable of delegating to subagents (e.g. gpt5.3-codex), or equivalent in another IDE
- **Models enabled** -- some models used by pipeline agents (e.g. `gpt-5.1-codex-max`) are hidden by default. Enable them in `Cursor Settings > Models`. See [Models | Cursor Docs](https://cursor.com/docs/models)

---

## Phase 0: Gitignore

**Goal**: Ensure generated and build artifacts are ignored by git.

**Grader check**:

```bash
./test-all.sh --phase 0
```

**Pass criteria**: `sandbox/node_modules/` and `**/tutorials/outputs/` are gitignored.

---

## Phase 1: Sandbox Project

**Goal**: The sandbox project exists, installs, and tests pass.

**Grader check**:

```bash
./test-all.sh --phase 1
```

**Pass criteria**:

| Check | Expected |
|-------|----------|
| `sandbox/package.json` exists | Yes |
| `sandbox/src/app.ts` exists | Yes |
| `npm test` | Exit 0 |
| `npm run typecheck` | Exit 0 |

---

## Phase 2: Foundation Tutorials (6 exercises)

**Goal**: All 6 Foundation exercises completed and verified.

**Target:** `docs/foundation/exercises/`

**Grader check**:

```bash
./test-all.sh --phase 2
```

Read each exercise file for full instructions. Summary of what to produce:

1. **Exercise 01 -- Vocabulary**: Read the Foundation README glossary. Write `tutorials/outputs/01-vocabulary.md` with `## <Term>` headings and original definitions for 9 terms (including State).
2. **Exercise 02 -- Pattern Recognition**: Read 4 scenarios. Write `tutorials/outputs/02-patterns.md` identifying the agent role and artifact for each.
3. **Exercise 03 -- Artifact Anatomy**: Read 3 walkthrough artifacts. Write `tutorials/outputs/03-annotations.md` annotating Writer, Required fields, and Consumer for each.
4. **Exercise 04 -- Trace Pipeline**: Write 3 pipeline artifacts to `.pipeline/HEALTH-01/`: `plan.json`, `worker-result.json`, `git-result.json`. Validate with `schema.py`.
5. **Exercise 05 -- Document Use Cases**: Write `tutorials/outputs/05-use-cases.md` with 3 use cases (task description, agent mapping, artifacts, why multi-agent).
6. **Exercise 06 -- Configuration Anatomy**: Read rules/skills/agents files. Write `tutorials/outputs/06-configuration.md` with `## Rules`, `## Skills`, `## Agents`, `## Quiz Answers` sections.

**Checkpoint:** `make phase-2` -- all 6 exercises PASS.

---

## Phase 3: Practitioner Tutorials (11 exercises)

**Goal**: All 11 Practitioner exercises completed using subagent delegation (exercises 02-05) and verified.

**Target:** `docs/practitioner/exercises/`

Exercises 02-05 MUST delegate to subagents via the `Task` tool. See **Delegation Requirements** above.

**Grader check**:

```bash
./test-all.sh --phase 3
```

1. **Exercise 01 -- Setup Project**: Copy `.cursor-practitioner/*` to `sandbox/.cursor/`. Run `npm test` and `npm run typecheck`.
2. **Exercise 02 -- Plan a Feature**: Use Task tool with `subagent_type: "jg-subplanner"` to write `sandbox/.pipeline/ISSUE-42/plan.json` for the auth middleware feature. The subplanner writes the artifact directly with `"produced_by": "jg-subplanner"`. The grader cross-references `affected_files` against the sandbox directory.
3. **Exercise 03 -- Implement Feature**: Use Task tool with `subagent_type: "jg-worker"` to implement auth login, middleware, and tests. The worker writes `sandbox/.pipeline/ISSUE-42/worker-result.json` with `"produced_by": "jg-worker"`. The grader verifies every `files_changed` entry exists on disk AND `npm test` passes.
4. **Exercise 04 -- Debug a Failure**: Introduce the expiry bug. Then use Task tool with `subagent_type: "jg-tester"` (writes `test-result-fail.json`), then `subagent_type: "jg-debugger"` (writes `debug-diagnosis.json`), then `subagent_type: "jg-worker"` (fixes the bug), then `subagent_type: "jg-tester"` again (writes `test-result-pass.json`). The grader verifies `npm test` passes.
5. **Exercise 05 -- Review and Ship**: Use Task tool with `subagent_type: "jg-reviewer"` (writes `review-result.json`) and `subagent_type: "jg-git"` (writes `git-result.json`). The grader verifies review findings reference real files on disk and the git branch exists. Also write `docs/practitioner/tutorials/outputs/05-hitl-analysis.md` with `## When to Block`, `## Approval Flow`, `## Risk Without HITL`.
6. **Exercise 06 -- Extend Pipeline**: Create `sandbox/.cursor/agents/team-linter.md` with frontmatter. Update `sandbox/.cursor/AGENTS.md`.
7. **Exercise 07 -- Author a Rule**: Copy rule template, create `sandbox/.cursor/rules/jg-test-before-commit.mdc` with valid frontmatter (`description`, `alwaysApply`) and body content.
8. **Exercise 08 -- Build a Skill**: Create `sandbox/.cursor/skills/jg-sandbox-test-runner/SKILL.md` with frontmatter (`name`, `description`) and body sections (When to Use, Running Tests, Interpreting Results, Writing Test Artifacts, Anti-patterns).
9. **Exercise 09 -- Understand Benchmarker**: Read `jg-benchmarker.md` and `jg-benchmark-ops/SKILL.md`. Write `docs/practitioner/tutorials/outputs/09-benchmarker-intro.md` with `## Benchmarker Role`, `## Verdict Definitions`, `## Per-Agent Focus`, `## When to Review`.
10. **Exercise 10 -- Resume Pipeline**: Create `sandbox/.pipeline/RESUME-01/state.yaml` with checkpoint for an interrupted pipeline (status: paused, current_stage: test). Write `docs/practitioner/tutorials/outputs/10-resume-analysis.md` with `## What the Planner Reads`, `## What Stages Are Skipped`, `## What Could Go Wrong`, `## Mitigation Strategies`.
11. **Exercise 11 -- Pipeline Observability**: Create `sandbox/.pipeline/ISSUE-42/pipeline-trace.json` reconstructing the execution timeline. Write `docs/practitioner/tutorials/outputs/11-observability-analysis.md` with `## Why Traces Matter`, `## Cost Visibility`, `## Failure Debugging`, `## Production Monitoring`.

**Checkpoint:** `make phase-3` -- all 11 exercises PASS. `npm test` passes in sandbox.

---

## Phase 4: Expert Tutorials (8 exercises)

**Goal**: All 8 Expert exercises completed with tiered subagent routing (exercises 02-03) and verified.

**Target:** `docs/expert/exercises/`

Exercises 02-03 MUST use the correct tiered subagents (fast/standard/high). See **Delegation Requirements** above.

**Grader check**:

```bash
./test-all.sh --phase 4
```

1. **Exercise 01 -- Classify Complexity**: Classify 5 tasks. Write `tutorials/outputs/01-classifications.json` with tier, signals, agents for each.
2. **Exercise 02 -- Tiered Pipeline**: Run 3 NOTIF issues through the pipeline. The grader cross-references `files_changed` in each `worker-result.json` against files on disk.
  - NOTIF-001 (trivial): Use Task tool with `subagent_type: "jg-worker-fast"`, `subagent_type: "jg-tester-fast"`, `subagent_type: "jg-reviewer-fast"`, `subagent_type: "jg-git"`. Write 5 artifacts to `sandbox/.pipeline/NOTIF-001/`.
  - NOTIF-002 (standard): Use Task tool with `subagent_type: "jg-subplanner"`, `subagent_type: "jg-worker"`, `subagent_type: "jg-tester"`, `subagent_type: "jg-reviewer"`, `subagent_type: "jg-git"`. Write 6 artifacts to `sandbox/.pipeline/NOTIF-002/`.
  - NOTIF-003 (complex): Use Task tool with `subagent_type: "jg-subplanner-high"`, `subagent_type: "jg-worker-high"`, `subagent_type: "jg-tester"`, `subagent_type: "jg-reviewer-high"`, `subagent_type: "jg-git"`. Write 6 artifacts to `sandbox/.pipeline/NOTIF-003/`.
3. **Exercise 03 -- Escalation Patterns**: Use Task tool with `subagent_type: "jg-worker-fast"` for NOTIF-002 scope (should return `status: "escalate"` and write a fast-tier worker-result). Then use `subagent_type: "jg-subplanner"` and `subagent_type: "jg-worker"` (standard). The grader verifies the fast-tier escalation artifact exists and `files_changed` entries are real.
4. **Exercise 04 -- Cost Analysis**: Write `tutorials/outputs/04-cost-analysis.json` with 3 strategies (all_standard, tiered_routing, standard_with_rework), costs, and recommendation.
5. **Exercise 05 -- Architecture Proposal**: Write `tutorials/outputs/05-architecture.md` with 7 sections (Agent Inventory, Pipeline Flow, Tier Routing Rules, Cost Projections, Monitoring Strategy, Escalation Policy, Rollback Plan).
6. **Exercise 06 -- Rules & Skills Design**: Write `tutorials/outputs/06-config-design.md` with `## Rules Design`, `## Skills Design`, `## Agent Inventory`, `## AGENTS.md Registry`, `## Activation Flow` (includes mermaid diagram).
7. **Exercise 07 -- Benchmark Review**: Use Task tool with `subagent_type: "jg-benchmarker"` to collect data and evaluate. Write `tutorials/outputs/07-benchmark-snapshot.json` (3+ model entries) and `tutorials/outputs/07-benchmark-report.md` (agent table with verdicts, recommendations, cost impact). The grader cross-references agent names against actual agent files in the repo.
8. **Exercise 08 -- Agent Evaluation**: Design plan quality rubric (5+ criteria) and review quality rubric (4+ criteria). Evaluate NOTIF-002 and NOTIF-003 plans. Write `tutorials/outputs/08-evaluation-rubrics.md` with `## Plan Quality Rubric`, `## Plan Evaluations`, `## Review Quality Rubric`, `## Improvement Recommendations`.

**Checkpoint:** `make phase-4` -- all 8 exercises PASS.

---

## Final Grading

```bash
./test-all.sh
```

All phases must report PASS. This confirms the entire course is completable and the verification scripts are correct.

---

## Pass Criteria Summary

| Phase | Pass condition |
|-------|----------------|
| 0 -- Gitignore | `sandbox/node_modules/` and `**/tutorials/outputs/` are gitignored |
| 1 -- Sandbox | Sandbox exists, `npm install`, `npm test`, `npm run typecheck` all succeed |
| 2 -- Foundation | All 6 exercises present, `verify.py --all` passes |
| 3 -- Practitioner | All 11 exercises present, subagent delegation used, `verify.py --all` passes, sandbox tests pass |
| 4 -- Expert | All 8 exercises present, tiered routing used where required, `verify.py --all` passes |

---

## Debugging Failures

- Read the `verify.py` output for the failing check name and details.
- For schema issues: `python3 .cursor-<tier>/pipeline/schema.py --validate <path>`
- For stage-gate issues: `python3 sandbox/.cursor/pipeline/check.py --issue <ID> --stage <stage>`
- For a single exercise: `python3 docs/<tier>/tutorials/verify.py --exercise N`
