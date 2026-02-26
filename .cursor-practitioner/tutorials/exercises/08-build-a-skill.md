# Exercise 08: Build a Reusable Skill

## Objective

Create a new reusable skill with a `SKILL.md` file. This tests understanding of the skill format, frontmatter, and how skills provide on-demand context to agents.

## Required Reading

- [Practitioner README](../../README.md) -- Skills section
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- Official Cursor docs on `SKILL.md` format, skill discovery, and activation by description matching
- [Agent Skills Guide](https://design.dev/guides/claude-skills/) -- SKILL.md format, dynamic context discovery
- Review the existing skill: `sandbox/.cursor/skills/jg-pipeline-artifact-io/SKILL.md`

> **Claude Code**: Claude Code uses the identical `SKILL.md` format in `.claude/skills/`. Skills are portable between Cursor and Claude Code with no changes -- just move the skill folder. The frontmatter fields (`name`, `description`) and body structure you create here work in both systems.

## Context

The sandbox has 2 existing skills (`jg-pipeline-artifact-io` and `jg-benchmark-ops`). You will add a 3rd skill that teaches agents how to run and interpret the sandbox test suite.

## Tasks

1. Create the skill directory:
   ```bash
   mkdir -p sandbox/.cursor/skills/jg-sandbox-test-runner
   ```

2. Create `sandbox/.cursor/skills/jg-sandbox-test-runner/SKILL.md` with this frontmatter:
   ```yaml
   ---
   name: jg-sandbox-test-runner
   description: "Run sandbox test suite and report results. Use when verifying sandbox code changes."
   ---
   ```

3. Fill in the body with these sections:

   **# JG Sandbox Test Runner** -- Title

   **## When to Use** -- Use this skill when any agent needs to verify that sandbox code changes pass the test suite. Typically invoked by `jg-tester` or `jg-worker` after implementation.

   **## Running Tests** -- How to execute: `cd sandbox && npm test`. Expected output format. What exit code 0 vs non-zero means.

   **## Interpreting Results** -- How to read Jest output: test count, pass/fail breakdown, error messages, stack traces.

   **## Writing Test Artifacts** -- After running tests, write results to `.pipeline/<issue-id>/test-result.json` with the schema: `{ "verdict": "PASS"|"FAIL", "phase_1": { "tool": "jest", "exit_code": N, "summary": "..." } }`.

   **## Anti-patterns** -- Do not skip tests for "simple" changes. Do not mark verdict as PASS if any test fails.

4. Verify the skill sits alongside the existing skills:
   ```bash
   ls sandbox/.cursor/skills/
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 08
```

Checks: file exists, has valid frontmatter with `name:` and `description:`, body has sufficient content, mentions test commands.

## Reflection

- How does the agent decide when to load this skill vs. the pipeline-artifact-io skill?
- What would you add to the `description` field to make activation more precise?
- Could this skill be shared across multiple projects? What would you change?
