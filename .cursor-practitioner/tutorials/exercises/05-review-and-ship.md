# Exercise 05: Review and Ship

## Objective

Delegate to the reviewer and git subagents to complete the pipeline.

## Required Reading

- [Reviewing and Testing Code | Cursor Learn](https://cursor.com/learn/reviewing-and-testing-code) -- Code review patterns with agents
- [Pipeline README](../../pipeline/README.md) -- review-result.json and git-result.json schemas
- [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How the `jg-reviewer` and `jg-git` agents are defined with readonly mode and specific roles

> **Claude Code**: The review-and-ship stage uses `jg-reviewer` (which reads code diffs and produces a verdict) and `jg-git` (which handles branching and commits). In Claude Code, these map to sequential prompts with appropriate models. The stage-gate validation via `check.py` is a standalone script that works in any environment.

## Context

Tests pass (Exercise 04 complete). The pipeline is at the review stage.

## Tasks

1. **Delegate to `jg-reviewer`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/plan.json` and `sandbox/.pipeline/ISSUE-42/worker-result.json`. Review the diff of changed files in `sandbox/src/auth/`. Write `sandbox/.pipeline/ISSUE-42/review-result.json` with verdict, blockers, concerns, nits, and `"produced_by": "jg-reviewer"`.

2. **Delegate to `jg-git`** with this prompt:
   > Create branch `feature/issue-42-auth-middleware`. Commit all changes in `sandbox/` with message `feat(auth): add login endpoint and JWT middleware`. Write `sandbox/.pipeline/ISSUE-42/git-result.json` with branch, commit_sha, commit_message, and `"produced_by": "jg-git"`.

3. **Run stage-gate validation** -- verify the pipeline's stage ordering invariants:
   ```bash
   python3 sandbox/.cursor/pipeline/check.py --issue ISSUE-42 --stage review
   ```
   This runs `check.py` to confirm that the review stage's preconditions are met (plan exists, worker completed, test passed before review).

4. Verify artifacts:
   ```bash
   python3 sandbox/.cursor/pipeline/schema.py --validate sandbox/.pipeline/ISSUE-42/review-result.json
   python3 sandbox/.cursor/pipeline/schema.py --validate sandbox/.pipeline/ISSUE-42/git-result.json
   git -C sandbox branch --list 'feature/issue-42*'  # branch should exist
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 05
```

Checks: review-result and git-result exist and pass schema, check.py stage-gate passes, git branch exists.

## Part 2: Human-in-the-Loop Approval

Production pipelines often require human approval before shipping. The reviewer can output a verdict of `blocked_pending_approval` when the change is correct but touches sensitive areas (security, database schema, public API) that require explicit human sign-off.

### Task

Write `tutorials/outputs/05-hitl-analysis.md` with these sections:

1. **When to block** -- List at least 3 categories of changes that should require human approval before the git step runs (e.g., security-sensitive code, breaking API changes, database migrations).
2. **Approval flow** -- Describe what happens when the reviewer outputs `blocked_pending_approval`: how does the planner handle it? What information should the approval request contain? Who approves?
3. **Risk without HITL** -- What could go wrong if every pipeline ran fully autonomously with no human checkpoints?

### Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 05
```

Checks (in addition to the Part 1 checks): `05-hitl-analysis.md` exists with 3 sections, each with sufficient depth.

## Reflection

- What did the reviewer flag? Were the nits reasonable?
- Is the commit message following conventional format?
- What would happen if the reviewer returned blockers?
- How would you configure which types of changes require human approval?
