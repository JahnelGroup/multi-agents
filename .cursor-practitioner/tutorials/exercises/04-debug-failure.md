# Exercise 04: Debug a Failure

## Objective

Experience the full failure/diagnosis/fix cycle by delegating to tester, debugger, and worker subagents.

## Required Reading

- [Finding and Fixing Bugs | Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) -- How agents discover, diagnose, and fix bugs
- [Practitioner walkthrough narrative](../../walkthrough/narrative.md) -- steps 4-9
- [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How the `jg-tester`, `jg-debugger`, and `jg-worker` agents are defined and dispatched

> **Claude Code**: The tester/debugger/worker cycle demonstrated here is a core multi-agent pattern. In Claude Code, each role would be a sequential prompt with the appropriate model. The artifact chain (test-result-fail.json -> debug-diagnosis.json -> fix -> test-result-pass.json) is the same -- artifacts are the coordination protocol regardless of IDE.

## Context

The auth feature from Exercise 03 is implemented and tests pass. We will introduce a bug to simulate a real debugging scenario.

## Tasks

1. **Introduce the bug**: In `sandbox/src/auth/middleware.ts`, change the JWT expiry comparison so that expired tokens are incorrectly accepted. For example, change `>` to `<` in the expiry check, or remove the expiry validation entirely.

2. Verify the bug causes test failure:
   ```bash
   cd sandbox && npm test  # should fail
   ```

3. **Delegate to `jg-tester`** with this prompt:
   > Run `npm test` in `sandbox/`. Capture the results. Write `sandbox/.pipeline/ISSUE-42/test-result-fail.json` with `verdict: "FAIL"`, details about which tests failed, and `"produced_by": "jg-tester"`.

4. **Delegate to `jg-debugger`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/test-result-fail.json`. Inspect the source files in `sandbox/src/auth/`. Identify the root cause. Write `sandbox/.pipeline/ISSUE-42/debug-diagnosis.json` with failure_source, root_cause, root_cause_file, root_cause_line, classification, and `"produced_by": "jg-debugger"`.

5. **Delegate to `jg-worker`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/debug-diagnosis.json`. Apply the fix to the identified file. The diagnosis should point to the JWT expiry comparison in middleware.ts.

6. **Delegate to `jg-tester`** again:
   > Run `npm test` in `sandbox/`. Write `sandbox/.pipeline/ISSUE-42/test-result-pass.json` with `verdict: "PASS"` and `"produced_by": "jg-tester"`.

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
