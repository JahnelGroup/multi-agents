# JG Pipeline — Artifact contract

All pipeline state lives under `.pipeline/<issue-id>/`.

## Quick reference

| Artifact | Writer | Required keys |
|----------|--------|---------------|
| plan.json | jg-subplanner | affected_files, steps, acceptance_mapping |
| worker-result.json | jg-worker | status, files_changed, blockers, summary |
| test-result.json | jg-tester | verdict, phase_1 |
| review-result.json | jg-reviewer | verdict, blockers, concerns, nits |
| debug-diagnosis.json | jg-debugger | failure_source, failure_description, root_cause, root_cause_file, root_cause_line, classification |
| git-result.json | jg-git | branch, commit_sha, commit_message |

## Directory layout

```
.pipeline/
  <issue-id>/
    plan.json
    worker-result.json
    test-result.json
    review-result.json
    debug-diagnosis.json
    git-result.json
    state.yaml   (optional; planner state)
  completed/     (optional; archived runs)
  lessons.yaml   (optional; cross-run failure patterns, planner reads at start)
```

## Artifacts (required fields)

### plan.json (jg-subplanner)

- `affected_files`: string[]
- `steps`: array of `{ order, action, file, description, rationale?, depends_on? }`
- `acceptance_mapping`: { string: string }
- `commit_plan?`: string[]
- `self_assessment?`: `{ confidence, uncertainty_areas, recommendation }`

### worker-result.json (jg-worker)

- `status`: "completed" | "blocked"
- `files_changed`: string[]
- `blockers`: string[]
- `summary`: string
- `self_assessment?`: as above

### test-result.json (jg-tester)

- `verdict`: "PASS" | "FAIL" | "SKIP"
- `phase_1`: { check_name: { result, output? } }
- `phase_2?`: { checks?, stack_trace?, reproduction?, timing_ms? }
- `classification?`: null (debugger sets); or "fix_target" if inline_triage
- `inline_triage?`: boolean
- `fix_instruction?`: string (when inline_triage)
- `self_assessment?`: as above

### review-result.json (jg-reviewer)

- `verdict`: "PASS" | "FAIL" | "SKIP"
- `blockers`: [{ file, line, description, fix }]
- `concerns`: same shape
- `nits`: same shape
- `trim_instructions?`: string
- `self_assessment?`: as above

### debug-diagnosis.json (jg-debugger)

- `failure_source`, `failure_description`, `root_cause`, `root_cause_file`, `root_cause_line`
- `classification`: "fix_target" | "plan_defect" | "escalate"
- `escalation_sub?`: "technical_complexity" | "ambiguous_requirement"
- `fix_instructions?`, `plan_fix_instructions?`
- `related_failures?`: string[]
- `self_assessment?`: as above

### git-result.json (jg-git)

- `branch`, `commit_sha`, `commit_message`
- `pr_number?`, `pr_url?`, `ci_status?`
- `downstream_unblocked?`: string[]
- `self_assessment?`: as above

### state.yaml (optional; jg-planner)

Planner state for resume and long-running work. Not validated by schema.py. Shape:

- `issue`, `issue_number`, `status` (in_progress | completed | failed | paused), `current_stage` (triage | plan | implement | test | review | git)
- `acceptance_criteria`: list of `{ id, text, test_mapped?, status }`
- `stages`: map of stage id to `{ agent, result, summary, artifact_path? }`
- `retries`, `routing_decisions`, `running_summary` (optional)

See **templates/state.yaml.example**.

### lessons.yaml (optional)

Cross-run failure patterns. Planner may read at pipeline start. Schema: list of `{ date, issue, pattern, frequency?, mitigation? }`. See **templates/lessons.yaml.example**. Not validated by schema.py.

## Stage-gate invariant checker

From repo root (or pass `--pipeline-dir` to point at a different `.pipeline`):

```bash
python .cursor/pipeline/check.py --issue <issue-id> --stage plan
python .cursor/pipeline/check.py --issue <issue-id> --stage implement
python .cursor/pipeline/check.py --issue <issue-id> --stage test
python .cursor/pipeline/check.py --issue <issue-id> --stage review
```

Checks: plan (affected_files, steps, acceptance_mapping, file/step consistency); implement (changed files vs plan scope); test (phase_2 gated on phase_1, classification); review (verdict vs blockers, finding file/line).

## Validation

From repo root:

```bash
python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/plan.json
```

Replace `plan.json` with the artifact filename. Projects may replace or extend `schema.py` with project-specific validation.
