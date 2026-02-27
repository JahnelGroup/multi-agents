# Exercise 04: Trace Pipeline

## Objective

Produce the complete 3-artifact chain for the "Add a health check endpoint" scenario from Foundation README.

## Required Reading

- [Foundation README](../../README.md) -- "Traced scenario" section
- [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- End-to-end feature flow with agents
- [Putting It All Together | Cursor Learn](https://cursor.com/learn/putting-it-together) -- How plans, implementations, and commits connect
- [Foundation Pipeline README](../../pipeline/README.md) -- artifact schemas
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- The `jg-pipeline-artifact-io` skill defines where and how agents read/write artifacts

> **Claude Code**: The artifact chain (plan.json -> worker-result.json -> git-result.json) is IDE-independent. These JSON files are the portable coordination protocol between agents, whether dispatched via Cursor's `Task` tool or Claude Code's sequential prompting.

## Scenario

Issue #5: Add GET /health endpoint that returns `{ status: 'ok' }`.

## Tasks

1. Create directory `.pipeline/HEALTH-01/` **at the repository root** (i.e., `<repo-root>/.pipeline/HEALTH-01/`, NOT inside `sandbox/`)
2. Write `.pipeline/HEALTH-01/plan.json` with `affected_files`, `steps`, and `acceptance_mapping`
3. Write `.pipeline/HEALTH-01/worker-result.json` with `status`, `files_changed`, `blockers`, and `summary`
4. Write `.pipeline/HEALTH-01/git-result.json` with `branch`, `commit_sha`, and `commit_message`

Create valid artifacts from scratch. Do NOT copy from the Foundation README inline examples.

**Artifact format**: Each JSON artifact must contain the required keys listed above. The `steps` array in `plan.json` must have entries with `step` (number), `file` (path string), and `description` (string). Every file in `affected_files` must appear in at least one step, and vice versa.

## Validation

```bash
python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/plan.json
python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/worker-result.json
python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/git-result.json
python3 .cursor-foundation/tutorials/verify.py --exercise 04
```

All schema validations must print `OK`.
