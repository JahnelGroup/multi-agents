# Build a Skill -- Reference Solution

## SKILL.md

```yaml
---
name: jg-sandbox-test-runner
description: "Run sandbox test suite and report results. Use when verifying sandbox code changes."
---
```

### Body

```markdown
# JG Sandbox Test Runner

## When to Use

Use this skill when any agent needs to verify that sandbox code changes pass the test suite. Typically invoked by `jg-tester` or `jg-worker` after implementation.

## Running Tests

Execute the test suite:

```bash
cd sandbox && npm test
```

- Exit code 0 = all tests passed
- Non-zero exit code = at least one test failed
- The command runs Jest via the `test` script in `package.json`

## Interpreting Results

Jest output includes:
- **Test suites**: Number of test files run, passed, and failed
- **Tests**: Individual test count with pass/fail breakdown
- **Error messages**: For failures, includes the assertion message, expected vs received values, and a stack trace pointing to the failing line

## Writing Test Artifacts

After running tests, write results to `.pipeline/<issue-id>/test-result.json`:

```json
{
  "verdict": "PASS" | "FAIL",
  "phase_1": {
    "tool": "jest",
    "exit_code": 0,
    "summary": "X tests passed, Y failed"
  },
  "produced_by": "jg-tester"
}
```

## Anti-patterns

- Do not skip tests for "simple" changes -- all changes go through verification
- Do not mark verdict as PASS if any test fails
- Do not run tests outside the sandbox directory
```

## Key design decisions

- `description` is specific enough for accurate activation: mentions "sandbox" and "test suite"
- Sections cover the full lifecycle: when to use, how to run, how to interpret, how to report
- Anti-patterns prevent common shortcuts that would undermine pipeline integrity
