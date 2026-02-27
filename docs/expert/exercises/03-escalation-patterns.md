# Exercise 03: Escalation Patterns

## Objective

Demonstrate the escalation flow by starting NOTIF-002 at the wrong tier (fast) and handling the escalation to standard.

!!! warning "Tiered Routing Required"
    This exercise **must** use the correct tiered subagent_types. Trivial issues use `jg-worker-fast`, `jg-tester-fast`, `jg-reviewer-fast`. Standard issues use `jg-subplanner`, `jg-worker`, `jg-tester`, `jg-reviewer`. Complex issues use `jg-subplanner-high`, `jg-worker-high`, `jg-reviewer-high`. The grader verifies tier routing.

!!! note "Required Reading"
    - [Expert README](../index.md) -- "Routing and escalation" section
    - [Expert walkthrough routing log](../walkthrough/routing-log.md) -- NOTIF-002 escalation event
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How agent tiers (fast/standard/high) map to different model assignments
    - [Finding and Fixing Bugs | Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) -- Debugging workflows relevant to diagnosing escalation triggers

=== "Cursor"
    Escalation patterns are framework-agnostic. The `escalation_history` array in artifacts works identically in Claude Code. The key difference is invocation: Cursor uses the `Task` tool to dispatch tiered subagents, while Claude Code uses sequential prompting with explicit model selection to achieve the same tier upgrade.

=== "Claude Code"
    Escalation patterns are framework-agnostic. The `escalation_history` array in artifacts works identically in Claude Code. The key difference is invocation: Cursor uses the `Task` tool to dispatch tiered subagents, while Claude Code uses sequential prompting with explicit model selection to achieve the same tier upgrade.

## Context

NOTIF-002 (notification service) was initially misclassified as trivial. The fast-tier worker recognizes it exceeds scope and requests escalation.

## Tasks

1. Create `sandbox/.pipeline/NOTIF-002-escalation/`

2. **Delegate to `jg-worker-fast`** with the NOTIF-002 scope (4 files, cross-service integration). The worker should recognize this exceeds fast tier and return `status: "escalate"` with `tier_used: "fast"`.

3. Read the escalation result. As the planner, decide to upgrade to standard tier.

4. **Delegate to `jg-subplanner`**: write `plan.json` for NOTIF-002.

5. **Delegate to `jg-worker`** (standard): implement the feature. Write `worker-result.json` with:

??? example "Expected Output"
    ```json
    {
      "status": "completed",
      "tier_used": "standard",
      "produced_by": "jg-worker",
      "escalation_history": [
        {
          "from_tier": "fast",
          "to_tier": "standard",
          "reason": "Multi-file change with cross-service integration exceeds fast scope"
        }
      ]
    }
    ```

!!! success "Validation"
    ```bash
    python3 docs/expert/tutorials/verify.py --exercise 03
    ```

    Checks: worker-result.json exists, has escalation_history, from_tier is "fast", to_tier is "standard", `produced_by` is "jg-worker".

??? question "Reflection"
    - What signals told the fast-tier worker to escalate?
    - How should the planner log escalation events for cost tracking?
    - What's the cost of a misclassification vs the cost of always using the highest tier?

??? success "Answer"
    **Fast-tier escalation**: When `jg-worker-fast` returns `status: "escalate"` because the task exceeds single-file scope:

    ```json
    {
      "status": "escalate",
      "tier_used": "fast",
      "blockers": ["Task scope exceeds fast tier: 4 files with cross-service integration"],
      "summary": "Requesting escalation to standard tier."
    }
    ```

    **Standard-tier completion after escalation**: The planner re-dispatches with `jg-worker` (standard), which completes the task. The `worker-result.json` should include `escalation_history` tracking the tier upgrade.

    Key: escalation is NOT counted as a retry. It is a normal routing mechanism.
