# Practitioner Tutorials

Hands-on exercises that require delegating tasks to multi-agent subagents. You will set up a real project, plan a feature, implement it, debug a failure, review and ship, and extend the pipeline.

## Prerequisites

- Python 3.10+ (for verify.py, schema.py, check.py)
- Node.js 18+ (for sandbox project)
- Sandbox project created and working (`sandbox/` at repo root, `npm test` passes)

## Critical Requirement: Subagent Delegation

Exercises 02-05 MUST be completed by delegating to the appropriate subagents via the `Task` tool, NOT by writing code or artifacts directly. This is the core point of the Practitioner tier: **experiment with multi-agent frameworks**.

In Cursor, delegation uses the `Task` tool with `subagent_type` set to the appropriate agent (e.g., `jg-subplanner`, `jg-worker`, `jg-tester`).

In Claude Code, the equivalent is sequential prompting with model selection per stage.

## Exercises

| # | Title | Subagents Used | Tests |
|---|-------|---------------|-------|
| 01 | [Setup Project](exercises/01-setup-project.md) | None (setup) | Directory structure, npm test |
| 02 | [Plan a Feature](exercises/02-plan-a-feature.md) | jg-subplanner | plan.json valid |
| 03 | [Implement Feature](exercises/03-implement-feature.md) | jg-worker | All tests pass, worker-result valid |
| 04 | [Debug a Failure](exercises/04-debug-failure.md) | jg-tester, jg-debugger, jg-worker | Fail/fix cycle, artifacts valid |
| 05 | [Review and Ship](exercises/05-review-and-ship.md) | jg-reviewer, jg-git | review-result, git-result valid |
| 06 | [Extend Pipeline](exercises/06-extend-pipeline.md) | None (manual) | team-linter agent created |

## Verification

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 01
python3 .cursor-practitioner/tutorials/verify.py --all
```

## Claude Code

Exercises use file operations, `Task` tool delegation, and CLI commands. In Claude Code, replace `Task` calls with sequential prompting to the appropriate model tier. The artifacts and validation commands are identical.
