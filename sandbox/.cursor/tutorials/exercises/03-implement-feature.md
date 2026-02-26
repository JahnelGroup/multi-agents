# Exercise 03: Implement Feature

## Objective

Delegate to the `worker` subagent to implement the auth feature according to the plan from Exercise 02.

## Required Reading

- [Finding and Fixing Bugs | Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) (preview for next exercise)
- [Pipeline README](../../pipeline/README.md) -- worker-result.json schema

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
   > - Write `sandbox/.pipeline/ISSUE-42/worker-result.json` with status, files_changed, blockers, summary

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
