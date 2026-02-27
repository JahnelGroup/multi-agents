# Pipeline — Artifact contract

All pipeline state lives under `.pipeline/<issue-id>/`.

The Foundation `schema.py` validator supports the full artifact set (plan, worker-result, test-result, review-result, debug-diagnosis, git-result) for forward compatibility. Foundation exercises only use the three artifacts below.

## Artifacts

### plan.json (planner writes)

- `affected_files`: string[] — files the worker should edit
- `steps`: array of { order, file, description } — ordered implementation steps
- `acceptance_mapping`: object — maps each acceptance criterion to a test or verification

### worker-result.json (worker writes)

- `status`: "completed" | "blocked"
- `files_changed`: string[]
- `blockers`: string[] — empty array when unblocked
- `summary`: string

### git-result.json (git writes)

- `branch`: string
- `commit_sha`: string
- `commit_message`: string
- `pr_url`: string (optional)
