# Exercise 04: Trace Pipeline

## Objective

Produce the complete 3-artifact chain for the "Add a health check endpoint" scenario from Foundation README.

## Required Reading

- [Foundation README](../../README.md) -- "Traced scenario" section
- [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features)
- [Putting It All Together | Cursor Learn](https://cursor.com/learn/putting-it-together)
- [Foundation Pipeline README](../../pipeline/README.md) -- artifact schemas

## Scenario

Issue #5: Add GET /health endpoint that returns `{ status: 'ok' }`.

## Tasks

1. Create directory `.pipeline/HEALTH-01/`
2. Write `plan.json` with `affected_files`, `steps`, and `acceptance_mapping`
3. Write `worker-result.json` with `status`, `files_changed`, `blockers`, and `summary`
4. Write `git-result.json` with `branch`, `commit_sha`, and `commit_message`

Create valid artifacts from scratch. Do NOT copy from the Foundation README inline examples.

## Validation

```bash
python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/plan.json
python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/worker-result.json
python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/git-result.json
python3 .cursor-foundation/tutorials/verify.py --exercise 04
```

All schema validations must print `OK`.
