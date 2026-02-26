# Exercise 05: Review and Ship

## Objective

Delegate to the reviewer and git subagents to complete the pipeline.

## Required Reading

- [Reviewing and Testing Code | Cursor Learn](https://cursor.com/learn/reviewing-and-testing-code)
- [Pipeline README](../../pipeline/README.md) -- review-result.json and git-result.json schemas

## Context

Tests pass (Exercise 04 complete). The pipeline is at the review stage.

## Tasks

1. **Delegate to `jg-reviewer`** with this prompt:
   > Read `sandbox/.pipeline/ISSUE-42/plan.json` and `sandbox/.pipeline/ISSUE-42/worker-result.json`. Review the diff of changed files in `sandbox/src/auth/`. Write `sandbox/.pipeline/ISSUE-42/review-result.json` with verdict, blockers, concerns, and nits.

2. **Delegate to `jg-git`** with this prompt:
   > Create branch `feature/issue-42-auth-middleware`. Commit all changes in `sandbox/` with message `feat(auth): add login endpoint and JWT middleware`. Write `sandbox/.pipeline/ISSUE-42/git-result.json` with branch, commit_sha, and commit_message.

3. Verify:
   ```bash
   python3 sandbox/.cursor/pipeline/schema.py --validate sandbox/.pipeline/ISSUE-42/review-result.json
   python3 sandbox/.cursor/pipeline/schema.py --validate sandbox/.pipeline/ISSUE-42/git-result.json
   git -C sandbox branch --list 'feature/issue-42*'  # branch should exist
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 05
```

Checks: review-result and git-result exist and pass schema, git branch exists.

## Reflection

- What did the reviewer flag? Were the nits reasonable?
- Is the commit message following conventional format?
- What would happen if the reviewer returned blockers?
