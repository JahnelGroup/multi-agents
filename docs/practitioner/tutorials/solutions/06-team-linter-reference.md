# Extend Pipeline -- Reference Solution

## team-linter.md

```yaml
---
name: team-linter
model: gemini-3-flash
description: Runs project linter and writes lint result; use when verifying code style before tests.
---
```

### Body

```markdown
# Team Linter

## ROLE

Runs the project linter and reports the result as a pipeline artifact. Inserted between the worker and tester stages.

## CORE RESPONSIBILITIES

- Read `plan.json` and `worker-result.json` to identify which files were changed
- Run `npm run lint` (or project-equivalent lint command)
- Write `.pipeline/<issue-id>/lint-result.json` with verdict and output

## OUTPUT

`.pipeline/<issue-id>/lint-result.json`:

```json
{
  "verdict": "PASS" | "FAIL",
  "output": "linter stdout/stderr",
  "errors": [],
  "produced_by": "team-linter"
}
```

## NON-GOALS

- Does not fix lint errors (that is the worker's job)
- Does not run tests (that is the tester's job)
- Does not modify source code
```

## AGENTS.md additions

Add to the agents table:
```
| **team-linter** | gemini-3-flash | Run linter before tests | plan.json, worker-result.json | lint-result.json |
```

Add to pipeline order:
```
3.5. **team-linter** -- After worker; writes `lint-result.json`. On FAIL → planner re-dispatches worker or escalates.
```

Add to subagent types:
```
- `linter` → team-linter
```
