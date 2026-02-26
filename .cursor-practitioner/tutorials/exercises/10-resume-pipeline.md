# Exercise 10: Resume a Pipeline from State

## Objective

Understand how pipelines use `state.yaml` to checkpoint progress and enable resumability. You will examine an interrupted pipeline, write a `state.yaml` that captures the checkpoint, and describe the decisions a planner would make to resume.

## Required Reading

- `.cursor-practitioner/templates/state.yaml.example` -- Reference format for state files
- `.cursor-practitioner/walkthrough/state.yaml` -- Completed state from the Issue-42 walkthrough
- `.cursor/skills/jg-pipeline-artifact-io/SKILL.md` -- Per-agent mapping and directory layout
- [Putting It Together | Cursor Learn](https://cursor.com/learn/putting-it-together) -- Multi-step workflows across agents

> **Claude Code**: State management concepts are IDE-agnostic. The `state.yaml` format and resume logic work identically in Claude Code sequential prompting.

## Context

Production pipelines get interrupted -- a model times out, CI hangs, or the user pauses work for the day. Without state, the planner must start from scratch: re-read the issue, re-plan, and risk re-implementing already-completed work. A `state.yaml` file lets the planner skip completed stages and resume from the exact point of interruption.

## Scenario

Issue RESUME-01 is a feature request: "Add rate limiting middleware to the Express app." The pipeline ran through planning and implementation but was interrupted during testing:

- **plan stage**: Completed. `plan.json` exists with `affected_files`, `steps`, and `acceptance_mapping`.
- **implement stage**: Completed. `worker-result.json` exists with `status: "completed"`.
- **test stage**: Interrupted. No `test-result.json` exists -- the tester was dispatched but the session ended before it could write results.

Your job: create the `state.yaml` that captures this checkpoint so the planner can resume.

## Tasks

### Part 1: Write the state file

Create `sandbox/.pipeline/RESUME-01/state.yaml` with the following content:

- `issue`: "Add rate limiting middleware"
- `issue_number`: 101
- `status`: "paused"
- `current_stage`: "test"
- At least 2 acceptance criteria with `status: "implemented"` (not yet verified because tests haven't run)
- `stages` section recording plan and implement as completed, with agent names and summaries
- `retries`: empty list
- `running_summary`: A sentence explaining where the pipeline stopped and what happens next

### Part 2: Write the resume analysis

Write to `tutorials/outputs/10-resume-analysis.md` explaining:

1. **What the planner reads** -- Which fields in `state.yaml` tell the planner where to resume?
2. **What stages are skipped** -- Which stages does the planner skip on resume, and why?
3. **What could go wrong** -- Name at least 2 risks of resuming (e.g., source code changed between sessions, stale plan)
4. **Mitigation strategies** -- For each risk, describe how the pipeline could detect or prevent the problem

## Output

1. `sandbox/.pipeline/RESUME-01/state.yaml` -- Valid YAML checkpoint file
2. `tutorials/outputs/10-resume-analysis.md` -- Resume analysis with the 4 sections above

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 10
```

Checks: `state.yaml` exists and is valid YAML with required fields (`issue`, `status`, `current_stage`, `stages`, `acceptance_criteria`). Analysis file exists with 4 sections, each with sufficient depth.
