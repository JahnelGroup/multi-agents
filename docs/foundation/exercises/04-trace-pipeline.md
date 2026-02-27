# Exercise 04: Trace Pipeline

## Objective

Produce the complete 3-artifact chain for the "Add a health check endpoint" scenario from Foundation README.

!!! note "Required Reading"
    - [Foundation README](../index.md) -- "Traced scenario" section (see [Walkthrough](../walkthrough.md))
    - [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- End-to-end feature flow with agents
    - [Putting It All Together | Cursor Learn](https://cursor.com/learn/putting-it-together) -- How plans, implementations, and commits connect
    - [Artifact Schemas](../../reference/artifacts.md) -- pipeline artifact schemas
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- The `jg-pipeline-artifact-io` skill defines where and how agents read/write artifacts

=== "Cursor"
    The exercises and validation below work in Cursor. Use the Cursor documentation links in Required Reading.

=== "Claude Code"
    The artifact chain (plan.json -> worker-result.json -> git-result.json) is IDE-independent. These JSON files are the portable coordination protocol between agents, whether dispatched via Cursor's `Task` tool or Claude Code's sequential prompting.

## Scenario

Issue #5: Add GET /health endpoint that returns `{ status: 'ok' }`.

## Tasks

1. Create directory `.pipeline/HEALTH-01/` **at the repository root** (i.e., `<repo-root>/.pipeline/HEALTH-01/`, NOT inside `sandbox/`)
2. Write `.pipeline/HEALTH-01/plan.json` with `affected_files`, `steps`, and `acceptance_mapping`
3. Write `.pipeline/HEALTH-01/worker-result.json` with `status`, `files_changed`, `blockers`, and `summary`
4. Write `.pipeline/HEALTH-01/git-result.json` with `branch`, `commit_sha`, and `commit_message`

Create valid artifacts from scratch. Do NOT copy from the Foundation README inline examples.

**Artifact format**: Each JSON artifact must contain the required keys listed above. The `steps` array in `plan.json` must have entries with `step` (number), `file` (path string), and `description` (string). Every file in `affected_files` must appear in at least one step, and vice versa.

!!! success "Validation"
    ```bash
    python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/plan.json
    python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/worker-result.json
    python3 .cursor-foundation/pipeline/schema.py --validate .pipeline/HEALTH-01/git-result.json
    python3 .cursor-foundation/tutorials/verify.py --exercise 04
    ```

    All schema validations must print `OK`.

??? success "Answer"
    Expected artifacts for the HEALTH-01 scenario:

    **plan.json**:
    ```json
    {
      "affected_files": ["src/routes/health.ts", "src/routes/health.test.ts"],
      "steps": [
        { "step": 1, "file": "src/routes/health.ts", "description": "Create GET /health route returning { status: 'ok' }" },
        { "step": 2, "file": "src/routes/health.test.ts", "description": "Test that GET /health returns 200 with expected body" }
      ],
      "acceptance_mapping": { "AC1_health_endpoint": "src/routes/health.ts" },
      "produced_by": "jg-subplanner"
    }
    ```

    **worker-result.json**:
    ```json
    {
      "status": "completed",
      "files_changed": ["src/routes/health.ts", "src/routes/health.test.ts"],
      "blockers": [],
      "summary": "Created health check endpoint and test",
      "produced_by": "jg-worker"
    }
    ```

    **git-result.json**:
    ```json
    {
      "branch": "feature/issue-5-health-endpoint",
      "commit_sha": "a1b2c3d",
      "commit_message": "feat: add GET /health endpoint",
      "produced_by": "jg-git"
    }
    ```

    Key: every file in `affected_files` must appear in a step, and vice versa. `blockers` must be an array (even if empty).
