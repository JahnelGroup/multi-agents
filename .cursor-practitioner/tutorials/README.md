# Practitioner Tutorials

Hands-on exercises that require delegating tasks to multi-agent subagents. You will set up a real project, plan a feature, implement it, debug a failure, review and ship, and extend the pipeline.

## Prerequisites

- Python 3.10+ (for verify.py, schema.py, check.py)
- Node.js 18+ (for sandbox project)
- Sandbox project created and working (`sandbox/` at repo root, `npm test` passes)

## Cursor Documentation

These exercises build on concepts covered in the official Cursor documentation:

| Topic | Link | Exercises |
|-------|------|-----------|
| Agent customization | [Customizing Agents - Cursor Learn](https://cursor.com/learn/customizing-agents) | 01, 06 |
| Custom agents & AGENTS.md | [Custom Agents - Cursor Docs](https://docs.cursor.com/agent/custom-agents) | 01, 04, 05, 06, 09 |
| Feature development | [Developing Features - Cursor Learn](https://cursor.com/learn/creating-features) | 02, 03 |
| Bug discovery & debugging | [Finding and Fixing Bugs - Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) | 03, 04 |
| Code review | [Reviewing and Testing Code - Cursor Learn](https://cursor.com/learn/reviewing-and-testing-code) | 05 |
| Rules (.mdc) | [Rules - Cursor Docs](https://docs.cursor.com/context/rules) | 01, 07 |
| Skills (SKILL.md) | [Agent Skills - Cursor Docs](https://docs.cursor.com/context/skills) | 01, 02, 08 |

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
| 07 | [Author a Rule](exercises/07-author-a-rule.md) | None (manual) | .mdc rule with valid frontmatter |
| 08 | [Build a Skill](exercises/08-build-a-skill.md) | None (manual) | SKILL.md with valid frontmatter |
| 09 | [Understand Benchmarker](exercises/09-understand-benchmarker.md) | None (conceptual) | Benchmarker role, verdicts, per-agent focus |
| 10 | [Resume Pipeline](exercises/10-resume-pipeline.md) | None (manual) | state.yaml checkpoint, resume analysis |
| 11 | [Pipeline Observability](exercises/11-pipeline-observability.md) | None (manual) | pipeline-trace.json, observability analysis |

## Verification

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 01   # single exercise
python3 .cursor-practitioner/tutorials/verify.py --all          # all 11 exercises
```

## Claude Code

Exercises use file operations, `Task` tool delegation, and CLI commands. In Claude Code, replace `Task` calls with sequential prompting to the appropriate model tier. The artifacts and validation commands are identical.
