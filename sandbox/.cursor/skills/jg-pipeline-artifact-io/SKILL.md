---
name: jg-pipeline-artifact-io
description: "Read/write layout for pipeline artifacts in .pipeline/. Use when any jg- agent reads upstream artifacts or writes its output."
---

# JG Pipeline Artifact I/O

## Directory layout

```
.pipeline/
  <issue-id>/
    state.yaml           # Planner state (optional)
    plan.json            # jg-subplanner
    worker-result.json   # jg-worker
    test-result.json     # jg-tester
    review-result.json   # jg-reviewer
    debug-diagnosis.json # jg-debugger
    git-result.json      # jg-git
  completed/             # Archive completed runs (optional)
  lessons.yaml           # Optional; cross-run failure patterns (planner reads at start)
```

## Setup

First agent that needs to write creates the directory:

```bash
mkdir -p .pipeline/<issue-id>
```

## Reading

- The planner supplies the artifact directory path in the dispatch prompt (e.g. `.pipeline/<issue-id>`).
- Read artifacts from disk; do not assume content is inline.
- Use `json.loads()` (or project equivalent) for JSON. If a file is missing, that stage has not run yet.

## Writing

- Write to the path given in the dispatch prompt. Ensure the parent directory exists.
- Serialize with `json.dumps(data, indent=2)` and a trailing newline.
- Include a `self_assessment` object in every artifact when the project expects it: `confidence` (0–1), `uncertainty_areas` (list), `recommendation` (string).

## Per-agent mapping

| Agent       | Reads                          | Writes              |
|------------|----------------------------------|---------------------|
| jg-subplanner | (issue)                        | plan.json           |
| jg-worker     | plan.json, debug-diagnosis.json | worker-result.json  |
| jg-tester     | (runs commands)                 | test-result.json    |
| jg-reviewer   | plan.json, worker-result.json   | review-result.json  |
| jg-debugger   | test-result.json, plan.json     | debug-diagnosis.json|
| jg-git        | (git)                           | git-result.json     |
| jg-planner    | all (read-only)                 | state.yaml if used  |

## Archive on completion

After jg-git finishes, optionally:

```bash
mkdir -p .pipeline/completed
mv .pipeline/<issue-id> .pipeline/completed/<issue-id>
```

Do not delete a run directory without archiving if you need history.

## Artifact shapes

See **pipeline/README.md** in this bundle for required fields and JSON shapes. Validate with **pipeline/schema.py**: from repo root, `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/<artifact>.json`.

## Anti-patterns

- Do not pass full artifact content in the prompt; pass the file path.
- Do not read an artifact before it exists; check for the file first.
- Do not delete `.pipeline/<issue-id>/` without archiving when runs must be kept.

**Lessons file:** Optional `.pipeline/lessons.yaml` holds cross-run failure patterns. Planner may read it at pipeline start. See **templates/lessons.yaml.example** in this bundle.
