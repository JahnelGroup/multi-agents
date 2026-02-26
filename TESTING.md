# Tutorial Test Plan

This document is the **canonical, rerunnable test plan** for the multi-agent training repo. An AI agent (e.g. gpt5.3-codex) can work through it from top to bottom to verify that each tier's tutorials, training content, and examples still work after changes.

**How to use**: Read this file and execute each phase in order. After each phase, confirm the pass criteria before moving on. To rerun from scratch, run the Reset Procedure first.

**Automated Agent Execution**: To have an AI agent systematically complete all exercises as a "student", you can use the provided Cursor plan: `@.cursor/plans/execute-training-course.plan.md`. Ask your agent to "execute this plan" to run through the entire curriculum and verify all outputs.

**Where tutorials live**: Each tier has a `tutorials/` directory with exercises and a `verify.py` script. Foundation is quiz-style; Practitioner and Expert are hands-on and require subagent delegation.

---

## Prerequisites

- **Python** 3.10+ (for `schema.py`, `check.py`, and each tier's `verify.py`)
- **Node.js** 20+ and **npm** (for the sandbox project)
- **git** (for branch/commit checks in Practitioner exercise 05)
- **Cursor** with an agent capable of delegating to subagents (e.g. gpt5.3-codex), or equivalent in another IDE

---

## Reset Procedure

Run these commands from the repo root to clean state from a previous test run. This makes the test idempotent.

```bash
# Remove pipeline and tutorial outputs
rm -rf .pipeline/
rm -rf .cursor-foundation/tutorials/outputs/
rm -rf .cursor-practitioner/tutorials/outputs/
rm -rf .cursor-expert/tutorials/outputs/
rm -rf sandbox/.pipeline/

# Reset sandbox to a clean state (if sandbox exists)
if [ -d sandbox ]; then
  rm -rf sandbox/node_modules/ sandbox/dist/
  # Optionally restore sandbox source only (if you want to keep the project but wipe exercise artifacts):
  # git checkout -- sandbox/
fi
```

After reset, the sandbox may need `npm install` again in Phase 2.

---

## Phase 0: Gitignore

**Goal**: Ensure generated and build artifacts are ignored by git.

**Steps**:

1. Open `.gitignore` at repo root.
2. Confirm it contains (or equivalent):
   - `.pipeline/`
   - `sandbox/node_modules/`
   - `sandbox/dist/`
   - `**/tutorials/outputs/`

**Verification** (from repo root):

```bash
git check-ignore -v sandbox/node_modules/package 2>/dev/null && echo "PASS: node_modules ignored" || echo "FAIL: node_modules not ignored"
git check-ignore -v .cursor-foundation/tutorials/outputs/foo 2>/dev/null && echo "PASS: tutorials/outputs ignored" || echo "FAIL: tutorials/outputs not ignored"
```

**Pass criteria**: Both checks print "PASS".

---

## Phase 1: Reframe READMEs

**Goal**: Confirm all READMEs use the competency framework (core question, analogy, expectation, portfolio, assessment).

**Steps**:

1. Read `README.md` — Tiers section must be the competency framework table (Core Question, Analogy, Expectation, Portfolio, Assessment, Contains). Getting Started must use competency-driven self-assessment. A "Tutorials" section must exist.
2. Read `.cursor-foundation/README.md` — Opening must say "This tier answers: Can you understand and use AI effectively?" and include the analogy. Sections: Tutorials, Portfolio, Assessment must exist.
3. Read `.cursor-practitioner/README.md` — Opening must say "This tier answers: Can you build and deploy AI features?" and the driving analogy. Sections: Tutorials, Portfolio, Assessment must exist.
4. Read `.cursor-expert/README.md` — Opening must say "This tier answers: Can you architect AI systems and lead others?" and the analogy. Sections: Tutorials, Portfolio, Assessment must exist.

**Pass criteria**: All four READMEs contain the competency framing and the three sections above. No automated script required; visual/manual check.

---

## Phase 2: Sandbox Project

**Goal**: The sandbox project exists, installs, and its single test passes.

**Steps**:

1. Confirm directory `sandbox/` exists with: `package.json`, `tsconfig.json`, `jest.config.ts`, `src/app.ts`, `src/app.test.ts`, `README.md`.
2. From repo root:
   ```bash
   cd sandbox && npm install && npm test && npm run typecheck
   ```
3. Expect: `npm test` runs 1 test (GET / returns 200) and exits 0; `npm run typecheck` exits 0.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| `sandbox/package.json` exists | Yes |
| `sandbox/src/app.ts` exists | Yes |
| `cd sandbox && npm test` | Exit 0, 1 test passed |
| `cd sandbox && npm run typecheck` | Exit 0 |

---

## Phase 3: Foundation Tutorials

**Goal**: All 5 Foundation exercises are present and verifiable; the agent can work through them and pass `verify.py --all`.

**Steps**:

1. Confirm `.cursor-foundation/tutorials/` exists with:
   - `README.md`
   - `exercises/01-vocabulary.md` through `05-document-use-cases.md`
   - `answers/` (answer keys for 01–03 and reference for 04)
   - `verify.py`
2. Work through each exercise in order (01 → 05). Write outputs to `.cursor-foundation/tutorials/outputs/` as specified in each exercise. For exercise 04, write artifacts to `.pipeline/HEALTH-01/`.
3. Run verification:
   ```bash
   python3 .cursor-foundation/tutorials/verify.py --all
   ```
4. Expect: All exercises report PASS.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| All 5 exercise markdown files exist | Yes |
| `verify.py` exists and runs | Yes |
| `verify.py --all` | All 5 exercises PASS |

---

## Phase 4: Practitioner Tutorials

**Goal**: All 6 Practitioner exercises exist; the agent completes them using **subagent delegation** (subplanner, worker, tester, debugger, reviewer, git) and all checks pass.

**Prerequisite**: Sandbox project (Phase 2) must be in place. Copy `.cursor-practitioner/` into `sandbox/.cursor/` as part of exercise 01.

**Steps**:

1. Confirm `.cursor-practitioner/tutorials/` exists with:
   - `README.md`
   - `exercises/01-setup-project.md` through `06-extend-pipeline.md`
   - `solutions/` (reference artifacts)
   - `verify.py`
2. Work through exercises 01–06 in order. For 02–05, **delegate** to the appropriate subagents; do not implement plan/worker/tester/reviewer/git outputs inline.
3. After each exercise (or at the end), run:
   ```bash
   cd sandbox && npm test
   ```
   (Re-run after 03, 04, 05 to confirm tests still pass.)
4. Run verification:
   ```bash
   python3 .cursor-practitioner/tutorials/verify.py --all
   ```
5. Expect: All 6 exercises PASS. Branch `feature/issue-42-auth-middleware` exists in sandbox. `sandbox/.cursor/agents/team-linter.md` exists (exercise 06).

**Pass criteria**:

| Check | Expected |
|-------|----------|
| All 6 exercise markdown files exist | Yes |
| `verify.py --all` | All 6 exercises PASS |
| `cd sandbox && npm test` | Exit 0 (all tests pass) |
| `sandbox/.pipeline/ISSUE-42/plan.json` (after 02) | Exists, valid per schema |
| `sandbox/.cursor/agents/team-linter.md` (after 06) | Exists, has frontmatter |

---

## Phase 5: Expert Tutorials

**Goal**: All 5 Expert exercises exist; the agent completes them with **tiered subagent routing** where required; all verifications pass.

**Prerequisite**: Sandbox and Practitioner exercises (Phases 2 and 4) should be done so the sandbox has the auth feature and pipeline layout. Expert exercises 02–03 add NOTIF-* pipeline runs.

**Steps**:

1. Confirm `.cursor-expert/tutorials/` exists with:
   - `README.md`
   - `exercises/01-classify-complexity.md` through `05-architecture-proposal.md`
   - `solutions/`
   - `verify.py`
2. Work through exercises 01–05. For 02 and 03, use the correct tiered subagents (e.g. jg-worker-fast, jg-worker, jg-worker-high) as specified.
3. Run verification:
   ```bash
   python3 .cursor-expert/tutorials/verify.py --all
   ```
4. Expect: All 5 exercises PASS.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| All 5 exercise markdown files exist | Yes |
| `verify.py --all` | All 5 exercises PASS |
| Expert artifact validation (tier_used, escalation_history where applicable) | Passes via verify.py |

---

## Pass Criteria Summary

| Phase | Pass condition |
|-------|----------------|
| 0 – Gitignore | `sandbox/node_modules/` and `**/tutorials/outputs/` are gitignored |
| 1 – READMEs | Root + 3 tier READMEs have competency framework and Tutorials/Portfolio/Assessment |
| 2 – Sandbox | Sandbox exists, `npm install`, `npm test`, `npm run typecheck` all succeed |
| 3 – Foundation | All 5 exercises present, `verify.py --all` passes |
| 4 – Practitioner | All 6 exercises present, subagent delegation used, `verify.py --all` passes, sandbox tests pass |
| 5 – Expert | All 5 exercises present, tiered routing used where required, `verify.py --all` passes |

---

## Rerun Notes

- **Full rerun**: Run Reset Procedure, then Phases 0 → 1 → 2 → 3 → 4 → 5 in order.
- **Subset**: To only re-verify tutorials without redoing implementation, run the relevant `verify.py --all` (e.g. `python3 .cursor-foundation/tutorials/verify.py --all`). This assumes outputs and artifacts from a previous run are still present.
- **Single exercise**: `python3 .cursor-<tier>/tutorials/verify.py --exercise N` (e.g. `--exercise 04`).
- **Debugging failures**: If a phase fails, read the `verify.py` output for the failing check. For schema validation, run `python3 .cursor/<tier>/pipeline/schema.py --validate <path>` manually. For Practitioner/Expert, ensure subagent delegation was actually used (verify.py may check transcripts or artifact provenance).
