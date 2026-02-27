# Exercise 04: Debug a Failure

## Objective

Experience the full failure/diagnosis/fix cycle by delegating to tester, debugger, and worker subagents.

!!! warning "Delegation Required"
    This exercise **must** use the Task tool with the specified `subagent_type`. Do not write pipeline artifacts manually. The grader cross-references `produced_by` fields and verifies files exist on disk.

!!! note "Required Reading"
    - [Finding and Fixing Bugs | Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) -- How agents discover, diagnose, and fix bugs
    - [Practitioner walkthrough narrative](../walkthrough/narrative.md) -- steps 4-9
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How the `jg-tester`, `jg-debugger`, and `jg-worker` agents are defined and dispatched

=== "Cursor"
    The tester/debugger/worker cycle uses Cursor's Task tool with the appropriate `subagent_type` for each agent.

=== "Claude Code"
    Each role would be a sequential prompt with the appropriate model. The artifact chain (test-result-fail.json -> debug-diagnosis.json -> fix -> test-result-pass.json) is the same -- artifacts are the coordination protocol regardless of IDE.

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

!!! success "Validation"
    ```bash
    python3 docs/practitioner/tutorials/verify.py --exercise 04
    ```

    Checks: test-result-fail, debug-diagnosis, and test-result-pass artifacts exist and pass schema validation. npm test passes.

??? question "Reflection"
    - How did the debugger identify the root cause? Was it accurate?
    - What information did the tester's failure report provide to help the debugger?
    - In a real pipeline, what happens if the debugger classifies the issue as `needs_human`?

??? success "Answer"
    The debug cycle produces 3 artifacts:

    **test-result-fail.json**: `verdict: "FAIL"` with details about which tests failed (JWT expiry check)

    **debug-diagnosis.json**: Should identify the root cause (changed comparison operator in expiry check), point to the specific file and line, and classify as `fix_target`

    **test-result-pass.json**: `verdict: "PASS"` after the worker applies the fix

    The key learning: the debugger reads the test failure, identifies the root cause in source code, and the worker applies a targeted fix. The pipeline retries testing after the fix.
