# Artifact Schemas

All pipeline state lives under `.pipeline/<issue-id>/`. Each agent reads upstream artifacts and writes its output to this directory. The planner supplies the artifact path in every dispatch.

## Artifact Overview

| Name | Writer | Consumer | Status |
|------|--------|----------|--------|
| plan.json | jg-subplanner | jg-worker, jg-reviewer | Required |
| worker-result.json | jg-worker | jg-reviewer, jg-tester | Required |
| test-result.json | jg-tester | jg-debugger, jg-planner | Required |
| review-result.json | jg-reviewer | jg-planner | Required |
| debug-diagnosis.json | jg-debugger | jg-worker, jg-subplanner, jg-planner | On failure |
| git-result.json | jg-git | jg-planner | Required |
| state.yaml | jg-planner | jg-planner | Optional |

## plan.json

**Writer:** jg-subplanner  
**Consumers:** jg-worker, jg-reviewer

**Required fields:** `affected_files`, `steps`, `acceptance_mapping`

**Optional:** `commit_plan`, `self_assessment`, `complexity` (Expert), `tier_used`, `cost_estimate`

??? example "plan.json"
    ```json
    {
      "affected_files": ["src/example/module.py", "tests/test_module.py"],
      "steps": [
        {
          "order": 1,
          "action": "modify",
          "file": "src/example/module.py",
          "description": "Add function X with default Y",
          "rationale": "AC-1: Implement X",
          "depends_on": []
        },
        {
          "order": 2,
          "action": "modify",
          "file": "tests/test_module.py",
          "description": "Add test for X",
          "rationale": "AC-1: Implement X",
          "depends_on": [1]
        }
      ],
      "acceptance_mapping": {"AC-1: Implement X": "tests/test_module.py::test_x"},
      "commit_plan": ["feat(ISSUE-123): add X"],
      "self_assessment": {"confidence": 0.9, "uncertainty_areas": [], "recommendation": "proceed to worker"}
    }
    ```

**Validation:** `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/plan.json`

## worker-result.json

**Writer:** jg-worker  
**Consumers:** jg-reviewer, jg-tester

**Required fields:** `status`, `files_changed`, `blockers`, `summary`

**Optional:** `self_assessment`, `tier_used`, `cost_estimate`, `escalation_history` (Expert)

??? example "worker-result.json"
    ```json
    {
      "status": "completed",
      "files_changed": ["src/example/module.py", "tests/test_module.py"],
      "blockers": [],
      "summary": "Implemented X and added test_x.",
      "self_assessment": {"confidence": 0.95, "uncertainty_areas": [], "recommendation": "proceed to tester"}
    }
    ```

**Validation:** `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/worker-result.json`

## test-result.json

**Writer:** jg-tester  
**Consumers:** jg-debugger, jg-planner

**Required fields:** `verdict`, `phase_1`

**Optional:** `phase_2`, `classification`, `inline_triage`, `fix_instruction`, `self_assessment`, `tier_used`, `cost_estimate`, `escalation_history` (Expert)

??? example "test-result.json"
    ```json
    {
      "verdict": "PASS",
      "phase_1": {
        "lint": {"result": "PASS", "output": null},
        "typecheck": {"result": "PASS", "output": null},
        "test": {"result": "PASS", "output": null}
      },
      "phase_2": null,
      "classification": null,
      "inline_triage": false,
      "self_assessment": {"confidence": 0.9, "uncertainty_areas": [], "recommendation": "proceed to reviewer"}
    }
    ```

**Validation:** `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/test-result.json`

## review-result.json

**Writer:** jg-reviewer  
**Consumers:** jg-planner

**Required fields:** `verdict`, `blockers`, `concerns`, `nits`

**Optional:** `trim_instructions`, `self_assessment`, `tier_used`, `cost_estimate`

??? example "review-result.json"
    ```json
    {
      "verdict": "PASS",
      "blockers": [],
      "concerns": [],
      "nits": [],
      "trim_instructions": null,
      "self_assessment": {"confidence": 0.9, "uncertainty_areas": [], "recommendation": "proceed to git"}
    }
    ```

**Validation:** `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/review-result.json`

## debug-diagnosis.json

**Writer:** jg-debugger  
**Consumers:** jg-worker, jg-subplanner, jg-planner

**Required fields:** `failure_source`, `failure_description`, `root_cause`, `root_cause_file`, `root_cause_line`, `classification`

**Optional:** `escalation_sub`, `fix_instructions`, `plan_fix_instructions`, `related_failures`, `self_assessment`, `tier_used`, `cost_estimate`

??? example "debug-diagnosis.json"
    ```json
    {
      "failure_source": "tester Phase 1",
      "failure_description": "test_x failed: AssertionError",
      "root_cause": "Wrong default value for Y",
      "root_cause_file": "src/example/module.py",
      "root_cause_line": "42",
      "classification": "fix_target",
      "escalation_sub": null,
      "fix_instructions": "Change default Y from 0 to 1 in module.py line 42.",
      "plan_fix_instructions": null,
      "related_failures": [],
      "self_assessment": {"confidence": 0.85, "uncertainty_areas": [], "recommendation": "re-dispatch to worker with fix_instructions"}
    }
    ```

**Validation:** `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/debug-diagnosis.json`

## git-result.json

**Writer:** jg-git  
**Consumers:** jg-planner

**Required fields:** `branch`, `commit_sha`, `commit_message`

**Optional:** `pr_number`, `pr_url`, `ci_status`, `downstream_unblocked`, `self_assessment`, `tier_used`, `cost_estimate`

??? example "git-result.json"
    ```json
    {
      "branch": "feature/issue-123-add-x",
      "commit_sha": "abc1234",
      "commit_message": "feat(ISSUE-123): add X",
      "pr_number": 42,
      "pr_url": "https://github.com/org/repo/pull/42",
      "ci_status": "pending",
      "downstream_unblocked": [],
      "self_assessment": {"confidence": 0.95, "uncertainty_areas": [], "recommendation": "PR opened; human to merge"}
    }
    ```

**Validation:** `python .cursor/pipeline/schema.py --validate .pipeline/<issue-id>/git-result.json`

## state.yaml

**Writer:** jg-planner  
**Consumer:** jg-planner (resume and tracking)

**Status:** Optional. Not validated by schema.py.

**Shape:** `issue`, `issue_number`, `status` (in_progress | completed | failed | paused), `current_stage` (triage | plan | implement | test | review | git), `acceptance_criteria`, `stages`, `retries`, `routing_decisions`, `running_summary`

??? example "state.yaml"
    ```yaml
    issue: "SPEC-X-002"
    issue_number: 42
    status: "in_progress"
    current_stage: "test"

    acceptance_criteria:
      - id: "AC-1"
        text: "Implement X per contract from SPEC-X-001"
        test_mapped: "tests/test_x.py::test_x_contract"
        status: "implemented"

    stages:
      plan:
        agent: "jg-subplanner"
        result: "PASS"
        summary: "Plan with 3 steps"
        artifact_path: ".pipeline/SPEC-X-002/plan.json"
      implement:
        agent: "jg-worker"
        result: "PASS"
        summary: "Implemented X and unit tests"
        artifact_path: ".pipeline/SPEC-X-002/worker-result.json"

    retries: []
    routing_decisions: []
    running_summary: "Plan and implement done; tester next."
    ```

## Tier Tracking Fields (Expert)

When using Expert tier routing, artifacts may include:

| Field | Type | Description |
|-------|------|-------------|
| tier_used | string | "fast" \| "standard" \| "high" — agent tier used for this artifact |
| cost_estimate | string | Human-readable cost estimate (e.g. tokens, $) |
| escalation_history | array | For worker-result.json and test-result.json only: `[{ from_tier, to_tier, reason }]` |

The stage-gate checker validates tier routing (e.g. complex tasks must not use fast-tier agents) and escalation_history tier progression.
