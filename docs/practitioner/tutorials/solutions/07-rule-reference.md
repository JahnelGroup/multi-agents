# Author a Rule -- Reference Solution

## jg-test-before-commit.mdc

```yaml
---
description: Require passing tests before jg-git commits
alwaysApply: false
---
```

### Body

```markdown
# JG Test Before Commit

## When to Apply

Apply when the pipeline reaches the git/commit stage for any issue-driven work.

## Rule

Before `jg-git` creates a branch or commit:

1. Verify that `test-result.json` exists in `.pipeline/<issue-id>/`
2. Verify the `verdict` field is `"PASS"`
3. If no test result exists or verdict is not PASS, block the commit and instruct the planner to re-dispatch `jg-tester`

## Exempt

Single-file documentation changes that do not affect runtime code (e.g., README updates, comment-only changes).
```

## Key design decisions

- `alwaysApply: false` because this rule only matters at the git stage, not during planning or implementation
- No `globs` field because the rule applies based on pipeline stage, not file type
- The exemption for docs-only changes prevents unnecessary test cycles for trivial updates
- The rule references `test-result.json` by the standard artifact name from the pipeline schema
