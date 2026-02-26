# Exercise 07: Author a Project Rule

## Objective

Create a new `.mdc` project rule from the template. This tests understanding of rule structure, frontmatter, and how rules guide agent behavior in the pipeline.

## Required Reading

- [Practitioner README](../../README.md) -- Rules section
- [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- `.mdc` format, frontmatter (description, alwaysApply, globs), precedence
- Review the existing rule: `sandbox/.cursor/rules/jg-planner-first.mdc`

> **Claude Code**: Claude Code handles project rules via `CLAUDE.md` at the repo root. The concept is the same -- persistent instructions that shape agent behavior -- but `.mdc` files offer per-concern separation with glob-based activation. The frontmatter fields you learn here (`description`, `alwaysApply`, `globs`) map to equivalent directives in Claude's system.

## Context

The sandbox project has 4 existing rules in `sandbox/.cursor/rules/`. You will add a 5th rule that enforces test execution before commits, teaching the pipeline to gate on test results.

## Tasks

1. Copy the rule template:
   ```bash
   cp sandbox/.cursor/templates/rule.mdc sandbox/.cursor/rules/jg-test-before-commit.mdc
   ```

2. Edit the frontmatter:
   ```yaml
   ---
   description: Require passing tests before jg-git commits
   alwaysApply: false
   ---
   ```

3. Fill in the body with these sections:

   **# JG Test Before Commit** -- Title

   **## When to Apply** -- Apply when the pipeline reaches the git/commit stage for any issue-driven work.

   **## Rule** -- Before `jg-git` creates a branch or commit:
   - Verify that `test-result.json` exists in `.pipeline/<issue-id>/`
   - Verify the `verdict` field is `"PASS"`
   - If no test result exists or verdict is not PASS, block the commit and instruct the planner to re-dispatch `jg-tester`

   **## Exempt** -- Single-file documentation changes that do not affect runtime code.

4. Verify the rule sits alongside the existing rules:
   ```bash
   ls sandbox/.cursor/rules/
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 07
```

Checks: file exists, has valid frontmatter with `description:` and `alwaysApply:`, has `## When to Apply` section, body has sufficient content.

## Reflection

- How would a planner agent discover and follow this rule at runtime?
- What happens if `alwaysApply` were set to `true`? When would that be appropriate?
- Could you add a `globs` field to restrict this rule to specific file types? When would that help?
