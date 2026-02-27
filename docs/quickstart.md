# Quickstart: Your First Pipeline in 5 Minutes

Get a multi-agent pipeline running in under 5 minutes. You'll paste a prompt, watch three agents collaborate, and inspect the artifacts they produce.

!!! note "Prerequisites"
    - [Cursor](https://cursor.com) installed with agent models enabled
    - Python 3.10+
    - Node.js 20+
    - git

## Step 1: Clone and set up

Clone the repo and install sandbox dependencies:

```bash
git clone https://github.com/JahnelGroup/multi-agents.git
cd multi-agents/sandbox
npm install
```

## Step 2: Run the pipeline

Open the `multi-agents` project in Cursor (the repo root, not the sandbox). Paste this prompt in the chat:

> "Work on issue HEALTH-01: Add GET /health endpoint that returns { status: 'ok' }."

Cursor reads the **jg-planner-first** rule and delegates to the planner. The planner orchestrates the pipeline: it dispatches a worker to implement the feature, then git to create a branch and commit.

## Step 3: What happened?

Three agents collaborated to turn an issue into a PR. Here's what each one did.

### Planner read the issue and wrote plan.json

The planner identified what needed to happen and wrote `.pipeline/HEALTH-01/plan.json`:

```json
{
  "affected_files": ["src/routes/health.ts", "src/routes/health.test.ts"],
  "steps": [
    { "order": 1, "file": "src/routes/health.ts", "description": "Create GET /health route returning { status: 'ok' }" },
    { "order": 2, "file": "src/routes/health.test.ts", "description": "Test that GET /health returns 200 with expected body" }
  ]
}
```

### Worker implemented the code and wrote worker-result.json

The planner dispatched jg-worker with the plan path. The worker read `plan.json`, created the files, and wrote `.pipeline/HEALTH-01/worker-result.json`:

```json
{
  "status": "completed",
  "files_changed": ["src/routes/health.ts", "src/routes/health.test.ts"],
  "summary": "Created health check endpoint and test"
}
```

### Git created a branch, committed, and wrote git-result.json

The planner dispatched jg-git. Git created a branch, wrote a conventional commit, opened a PR, and wrote `.pipeline/HEALTH-01/git-result.json`:

```json
{
  "branch": "feature/health-01-health-endpoint",
  "commit_sha": "a1b2c3d",
  "pr_url": "https://github.com/org/repo/pull/12"
}
```

!!! info "What just happened"
    Three agents collaborated to turn an issue into a PR. The **planner** read the issue and produced a plan. The **worker** implemented the code and tests. The **git** agent created a branch, committed, and opened a PR. Each agent wrote a JSON artifact that the next stage (or you) can inspect. You review and merge the PR when ready.

## Next steps

Ready to learn more?

- [Foundation](foundation/index.md) — understand agents, rules, and pipelines
- [Practitioner](practitioner/index.md) — hands-on pipeline use with testing and review
- [Expert](expert/index.md) — tiered routing, cost optimization, and architecture design
