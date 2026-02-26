# Pipeline — Artifact contract

All pipeline state lives under `.pipeline/<issue-id>/`.

## Artifacts

### plan.json (planner writes)

- `affected_files`: string[] — files the worker should edit
- `steps`: array of { order, file, description } — ordered implementation steps

### worker-result.json (worker writes)

- `status`: "completed" | "blocked"
- `files_changed`: string[]
- `summary`: string

### git-result.json (git writes)

- `branch`: string
- `commit_sha`: string
- `pr_url`: string
