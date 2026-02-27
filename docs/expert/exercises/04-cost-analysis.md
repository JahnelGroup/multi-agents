# Exercise 04: Cost Analysis

## Objective

Calculate and compare costs across 3 routing strategies using the NOTIF scenario.

!!! note "Required Reading"
    - [Expert walkthrough cost summary](../walkthrough/cost-summary.md)
    - [Expert README](../index.md) -- "Tiered model strategy" table
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How the `model` field in agent frontmatter determines cost per invocation
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- How the `jg-benchmark-ops` skill defines cost/performance evaluation workflows

=== "Cursor"
    Cost analysis applies equally to Claude Code deployments. Model pricing (input/output per token) and invocation counts are the same regardless of IDE. The tiered routing savings demonstrated here translate directly to model selection strategies in Claude Code's sequential prompting.

=== "Claude Code"
    Cost analysis applies equally to Claude Code deployments. Model pricing (input/output per token) and invocation counts are the same regardless of IDE. The tiered routing savings demonstrated here translate directly to model selection strategies in Claude Code's sequential prompting.

## Cost Model

| Tier | Tokens/invocation | Cost/invocation |
|------|------------------|-----------------|
| Fast | ~2,000 | ~$0.002 |
| Standard | ~8,000 | ~$0.03 |
| High | ~20,000 | ~$0.15 |

Each pipeline run involves: planner + subplanner + worker + tester + reviewer + git = ~6 agent invocations.

## Tasks

1. **Strategy A -- All Standard**: Route every issue (NOTIF-001, -002, -003) to standard tier.
2. **Strategy B -- Tiered Routing**: Route to appropriate tier (fast/standard/high) as in Exercise 02.
3. **Strategy C -- Standard with Rework**: Use standard for everything, but NOTIF-003 needs 1.5x retry cycles because standard tier cannot handle the complexity in one pass.

For each strategy, calculate:
- Total invocations (planner counts for standard/high only)
- Total tokens
- Total cost

Write an analysis explaining when tiered routing pays off vs overpaying for simple tasks.

## Output

Write to `tutorials/outputs/04-cost-analysis.json`:

??? example "Expected Output"
    ```json
    {
      "strategies": {
        "all_standard": {
          "total_invocations": 18,
          "total_tokens": 144000,
          "total_cost": 0.54,
          "notes": "Overpays for NOTIF-001 (trivial) by using standard agents"
        },
        "tiered_routing": {
          "total_invocations": 17,
          "total_tokens": 108000,
          "total_cost": 0.37,
          "notes": "Optimal -- fast for trivial, standard for standard, high for complex"
        },
        "standard_with_rework": {
          "total_invocations": 21,
          "total_tokens": 168000,
          "total_cost": 0.63,
          "notes": "Standard agents cannot handle NOTIF-003 complexity in one pass, requiring rework"
        }
      },
      "recommendation": "Tiered routing saves 31% vs all-standard and 41% vs standard-with-rework. The savings increase with higher task volume. For teams processing 20+ issues/week, tiered routing is clearly cost-effective.",
      "breakeven_analysis": "Tiered routing pays off when at least 40% of tasks are trivial (fast tier) or when complex tasks would require standard-tier rework. With our 33/33/33 mix, the savings are moderate but scale linearly."
    }
    ```

!!! success "Validation"
    ```bash
    python3 .cursor-expert/tutorials/verify.py --exercise 04
    ```

    Checks: valid JSON, 3 strategies present, required fields, recommendation >= 20 words, costs differ between strategies.
