# Trace Pipeline Solution

Expected artifacts for the "Add a health check endpoint" scenario (Issue #5 / HEALTH-01).

## plan.json

```json
{
  "affected_files": ["src/routes/health.ts", "src/routes/health.test.ts"],
  "steps": [
    {
      "step": 1,
      "file": "src/routes/health.ts",
      "description": "Create GET /health route that returns { status: 'ok' } with HTTP 200"
    },
    {
      "step": 2,
      "file": "src/routes/health.test.ts",
      "description": "Write tests verifying GET /health returns 200 with expected JSON body"
    }
  ],
  "acceptance_mapping": {
    "AC1_health_endpoint": "src/routes/health.ts",
    "AC2_response_body": "src/routes/health.test.ts"
  },
  "produced_by": "jg-subplanner"
}
```

Key points:
- Every file in `affected_files` has at least one step, and every step file is in `affected_files`
- Steps are ordered: implementation before tests
- `acceptance_mapping` links criteria to verifying files

## worker-result.json

```json
{
  "status": "completed",
  "files_changed": ["src/routes/health.ts", "src/routes/health.test.ts"],
  "blockers": [],
  "summary": "Created GET /health endpoint returning { status: 'ok' } and added test coverage",
  "produced_by": "jg-worker"
}
```

Key points:
- `status` must be "completed" (not "done" or "finished")
- `files_changed` matches what was actually modified
- `blockers` is an empty array, not omitted

## git-result.json

```json
{
  "branch": "feature/issue-5-health-endpoint",
  "commit_sha": "a1b2c3d",
  "commit_message": "feat: add GET /health endpoint",
  "produced_by": "jg-git"
}
```

Key points:
- Branch name follows conventional format
- Commit message uses conventional commit prefix
- `commit_sha` is a plausible short hash
