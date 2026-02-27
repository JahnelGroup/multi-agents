# Common Mistakes

These anti-patterns cause pipeline failures, grader rejections, or wasted effort. Avoid them when adopting the multi-agent pipeline.

### 1. Writing artifacts manually instead of delegating

!!! failure "Symptom"
    You write `plan.json` or `worker-result.json` directly instead of using the Task tool. The grader rejects the exercise.

**Cause:** Trying to shortcut the delegation process, or the subagent call failed and you wrote the artifact as a fallback.

**Fix:** Always use `Task(subagent_type="jg-subplanner", ...)` to have the subagent write its own artifacts. If the Task call fails, the exercise fails — do not fake artifacts.

### 2. Using the wrong `subagent_type`

!!! failure "Symptom"
    The planner invokes the wrong agent, or the grader reports a mismatch between the requested agent and the one that ran.

**Cause:** Passing an incorrect `subagent_type` (e.g. `jg-worker` when you meant `jg-subplanner`), or using a generic type instead of the specific jg- agent name.

**Fix:** Use the exact `subagent_type` specified in the exercise: `jg-subplanner`, `jg-worker`, `jg-tester`, `jg-reviewer`, `jg-debugger`, `jg-git`. Check AGENTS.md for the mapping.

### 3. Forgetting or faking the `produced_by` field

!!! failure "Symptom"
    The grader rejects an artifact because `produced_by` is missing, wrong, or doesn't match the agent that actually produced it.

**Cause:** Manually editing artifacts and inserting a `produced_by` value, or omitting it entirely. The grader cross-references metadata against actual filesystem state.

**Fix:** Only agents that actually produce an artifact should have their name in `produced_by`. Never fake it. If you delegated correctly, the subagent writes the field.

### 4. `files_changed` entries that don't exist on disk

!!! failure "Symptom"
    The grader fails because `worker-result.json` lists files that don't exist in the sandbox or project.

**Cause:** The worker reported changed files that were never written, or paths are incorrect (typos, wrong directory).

**Fix:** Ensure every file in `files_changed` exists on disk. The grader verifies this. If the worker made a mistake, re-dispatch to the worker — do not manually edit the artifact.

### 5. Model not enabled in Cursor settings

!!! failure "Symptom"
    The agent fails to run because the model specified in agent frontmatter is not available.

**Cause:** Some models (e.g. `gpt-5.1-codex-max`) are hidden by default in Cursor and must be enabled in Settings > Models.

**Fix:** Enable the required models in Cursor Settings > Models. If a model isn't available on your plan, substitute any available model and expect more retries from cheaper models.

### 6. Agent didn't pick up a rule (frontmatter issue)

!!! failure "Symptom"
    A rule exists in `.cursor/rules/` but the agent doesn't follow it.

**Cause:** Invalid frontmatter (missing `---` markers), missing or vague `description` field, or wrong file location. Cursor uses `description` to decide when to include the rule.

**Fix:** Ensure the file is in `.cursor/rules/`, has valid YAML frontmatter between `---` markers, and the `description` field accurately describes when it should apply.

### 7. Pipeline artifacts not appearing (directory not created)

!!! failure "Symptom"
    You expect artifacts under `.pipeline/<issue-id>/` but the directory doesn't exist.

**Cause:** The first agent that writes creates the directory. If you're starting fresh, the planner creates it. A misconfigured or failed first dispatch can leave it missing.

**Fix:** Verify the planner (or first agent in the pipeline) ran successfully. Check that the issue ID is correct and that the planner has write access to create `.pipeline/<issue-id>/`.

### 8. Delegating entire tiers to `generalPurpose` agents

!!! failure "Symptom"
    The grader rejects the exercise because a `generalPurpose` sub-agent was used instead of the specified jg- agents.

**Cause:** Dispatching to a generic agent and expecting it to further delegate to jg-subplanner, jg-worker, etc. A `generalPurpose` agent cannot further dispatch to jg- agents.

**Fix:** The top-level agent must dispatch each delegation exercise individually using the specified `subagent_type`. Do not delegate the whole tier to a single generic agent.

### 9. Under-tiering complex tasks (using standard for complex work)

!!! failure "Symptom"
    Complex tasks fail repeatedly, trigger multiple retries, or produce poor results. Cost and latency are higher than expected.

**Cause:** Classifying safety-critical work, new abstractions, or architectural changes as Standard instead of Complex. Standard-tier agents may lack the reasoning power for such work.

**Fix:** Use the tier routing table: Complex tasks go to jg-subplanner-high, jg-worker-high, jg-reviewer-high, jg-debugger-high. See jg-tier-routing.mdc for classification criteria.

### 10. Skipping the planner for multi-step work

!!! failure "Symptom"
    You invoke jg-worker, jg-tester, or jg-reviewer directly for issue-driven work. The pipeline breaks or produces inconsistent artifacts.

**Cause:** Bypassing the planner for multi-file edits, refactors, or issue-driven work. The planner orchestrates the full pipeline and handles failures.

**Fix:** For any multi-step implementation request (2+ files, plan-driven work, issue-driven work), your first tool call must be `Task(subagent_type="jg-planner", ...)`. The planner orchestrates subplanner → worker → tester → reviewer → git.
