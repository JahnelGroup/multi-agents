# Exercise 04: Debug a Failure

## Objective

Experience the full failure/diagnosis/fix cycle by delegating to tester, debugger, and worker subagents.

## Required Reading

- [Finding and Fixing Bugs | Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs)
- [Practitioner walkthrough narrative](../../walkthrough/narrative.md) -- steps 4-9

## Context

The auth feature from Exercise 03 is implemented and tests pass. We will introduce a bug to simulate a real debugging scenario.

## Tasks

1. **Introduce the bug**: In `sandbox/src/auth/middleware.ts`, change the JWT expiry comparison so that expired tokens are incorrectly accepted. For example, change `>` to `<` in the expiry check, or remove the expiry validation entirely.

2. Verify the bug causes test failure:
   ```bash
   cd sandbox && npm test  # should fail
   ```

3. **Delegate to `jg-tester`** with this prompt:
   > Run `npm test` in `sandbox/`. Capture the results. Write `sandbox/.pipeline/ISSUE-42/test-result-fail.json` with `verdict: "FAIL"` and details about which tests failed.

4. **Delegate to `jg-debugger`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/test-result-fail.json`. Inspect the source files in `sandbox/src/auth/`. Identify the root cause. Write `sandbox/.pipeline/ISSUE-42/debug-diagnosis.json` with failure_source, root_cause, root_cause_file, root_cause_line, and classification.

5. **Delegate to `jg-worker`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/debug-diagnosis.json`. Apply the fix to the identified file. The diagnosis should point to the JWT expiry comparison in middleware.ts.

6. **Delegate to `jg-tester`** again:
   > Run `npm test` in `sandbox/`. Write `sandbox/.pipeline/ISSUE-42/test-result-pass.json` with `verdict: "PASS"`.

7. Verify all tests pass:
   ```bash
   cd sandbox && npm test  # should pass after fix
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 04
```

Checks: test-result-fail, debug-diagnosis, and test-result-pass artifacts exist and pass schema validation. npm test passes.

## Reflection

- How did the debugger identify the root cause? Was it accurate?
- What information did the tester's failure report provide to help the debugger?
- In a real pipeline, what happens if the debugger classifies the issue as `needs_human`?
