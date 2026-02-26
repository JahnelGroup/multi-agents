# Exercise 03: Implement Feature

## Objective

Delegate to the `worker` subagent to implement the auth feature according to the plan from Exercise 02.

## Required Reading

- [Finding and Fixing Bugs | Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) -- Preview for the debug exercise; understanding bug discovery informs implementation quality
- [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- End-to-end feature implementation with agents
- [Pipeline README](../../pipeline/README.md) -- worker-result.json schema

> **Claude Code**: The worker agent reads `plan.json` and produces code + `worker-result.json`. This plan-to-implementation contract is the same in Claude Code -- the worker is a model prompt that reads the plan artifact and writes both code and the result artifact. The schema validation (`schema.py`) runs identically in either system.

## Context

The plan exists at `sandbox/.pipeline/ISSUE-42/plan.json`. The worker reads it and implements accordingly.

## Tasks

1. **Delegate to `jg-worker`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/plan.json`. Implement the auth feature in `sandbox/`:
   > - Create `sandbox/src/auth/login.ts` -- POST /auth/login endpoint using jsonwebtoken
   > - Create `sandbox/src/auth/middleware.ts` -- JWT validation middleware
   > - Create `sandbox/src/auth/login.test.ts` -- tests for valid login, invalid credentials
   > - Create `sandbox/src/auth/middleware.test.ts` -- tests for valid token, expired token, missing token
   > - Register the auth routes in `sandbox/src/app.ts`
   > - Write `sandbox/.pipeline/ISSUE-42/worker-result.json` with status, files_changed, blockers, summary, and `"produced_by": "jg-worker"`

2. Run tests:
   ```bash
   cd sandbox && npm test
   ```
   All tests must pass.

3. Verify the worker-result artifact:
   ```bash
   python3 sandbox/.cursor/pipeline/schema.py --validate sandbox/.pipeline/ISSUE-42/worker-result.json
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 03
```

Checks: worker-result.json exists, passes schema, npm test passes, auth source files exist.

## Reflection

- Did the worker follow the plan exactly, or did it deviate?
- Are the tests comprehensive? Do they cover edge cases?
- What would happen if the worker couldn't complete a step?
