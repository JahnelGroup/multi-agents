# Exercise 07: Run a Benchmark Review

## Objective

Delegate to `jg-benchmarker` to collect benchmark data, evaluate current model assignments for all sandbox agents, and produce an advisory recommendation report. This is the operational skill that keeps a multi-agent system current as models evolve.

!!! note "Required Reading"
    - `.cursor-expert/agents/jg-benchmarker.md` -- Full agent definition, per-agent benchmark focus, execution style
    - `.cursor-expert/skills/jg-benchmark-ops/SKILL.md` -- Collection/evaluation workflow, verdict definitions
    - `.cursor-expert/AGENTS.md` -- Agent registry with current model assignments
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How the `model` field in agent frontmatter controls model assignment
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- How skills like `jg-benchmark-ops` activate on-demand
    - [Agent Skills Guide](https://design.dev/guides/claude-skills/) -- Additional guide on skill activation and format

=== "Cursor"
    The benchmarker workflow uses Cursor's Task tool to dispatch `jg-benchmarker`. The snapshot format, verdict definitions, and recommendation structure are identical across environments.

=== "Claude Code"
    The benchmarker workflow is IDE-agnostic. In Claude Code, you would invoke the same collection and evaluation logic via sequential prompting with model selection. The snapshot format, verdict definitions, and recommendation structure are identical. Only the invocation mechanism differs (Task tool in Cursor vs. direct prompting in Claude Code).

## Context

Your sandbox has 9 agents (8 core pipeline + team-linter). Each has a `model:` field in its frontmatter. Over time, new models release, prices change, and capabilities shift. The benchmarker agent automates the research and evaluation so you can make data-driven decisions about model assignments.

This exercise teaches the Expert-level workflow: collect -> evaluate -> recommend -> (optionally) apply.

## Tasks

### Step 1: Collect Benchmark Data

**Delegate to `jg-benchmarker`** with this prompt:

> Collect the latest benchmark data for models currently used by our agents. Focus on models referenced in `sandbox/.cursor/agents/`. Store the snapshot at `.cursor-expert/tutorials/outputs/07-benchmark-snapshot.json`. Include scores for: reasoning, coding, instruction-following, speed, and pricing. Record the source URL and retrieval date for every score. Include `"produced_by": "jg-benchmarker"` in the snapshot JSON. Do not overwrite existing snapshots.

The snapshot should be structured JSON with entries per model, each containing benchmark scores and metadata.

### Step 2: Evaluate Current Assignments

**Delegate to `jg-benchmarker`** with this prompt:

> Using the snapshot at `.cursor-expert/tutorials/outputs/07-benchmark-snapshot.json`, evaluate the current model assignments for all agents listed in `sandbox/.cursor/agents/`. For each agent, determine which benchmarks are primary (use the per-agent benchmark focus table in your agent definition), compare the current model to alternatives, and assign a verdict (Excellent/Correct/Monitor/Tune/Upgrade). Write the evaluation report to `.cursor-expert/tutorials/outputs/07-benchmark-report.md`. Include a `Produced by: jg-benchmarker` line in the report header.

### Step 3: Review the Report

The report should include:

1. **Agent Evaluation Table**: Agent | Current Model | Verdict | Key Metrics (primary benchmark scores)
2. **Recommendations**: For any agent with verdict Monitor/Tune/Upgrade, suggest a specific model change with before/after metrics and cost impact
3. **Cost Impact Summary**: Total estimated monthly cost change if all recommendations were applied
4. **Overall Assessment**: Whether the current agent configuration is healthy or needs attention

### Step 4: Do NOT Apply Changes

The benchmarker is advisory by default. Review the recommendations but do not modify any agent files. In a real workflow, an Expert would review the report, discuss with the team, and then explicitly instruct the benchmarker to apply changes.

## Output

Two files in `.cursor-expert/tutorials/outputs/`:

- `07-benchmark-snapshot.json` -- Structured benchmark data with model scores, sources, and dates
- `07-benchmark-report.md` -- Evaluation report with agent table, recommendations, and cost impact

!!! success "Validation"
    ```bash
    python3 .cursor-expert/tutorials/verify.py --exercise 07
    ```

    Checks: snapshot JSON exists and is valid with `produced_by: "jg-benchmarker"`, report markdown exists with required sections (agent evaluation table, recommendations, cost impact) and `Produced by: jg-benchmarker` line, report mentions 5+ agent names, report references all 5 verdict terms, report has sufficient depth.

??? question "Reflection"
    - Which agents had the most room for improvement? Why?
    - Did any agent get a "Tune" verdict where a cheaper model outperforms? What's the cost savings?
    - How often should you rerun this review in a production environment?
    - What would change if a new model releases tomorrow that's 50% cheaper with similar performance?
    - How would you automate this review on a quarterly schedule?

??? success "Answer"
    **Snapshot** (07-benchmark-snapshot.json): Must include per-model entries with benchmark scores (reasoning, coding, instruction_following, speed), pricing, source URLs, and `produced_by: "jg-benchmarker"`.

    **Report** (07-benchmark-report.md): Must include agent evaluation table, recommendations for Monitor/Tune/Upgrade verdicts, cost impact summary, and overall assessment.

    **Typical verdicts**: Subplanner and debugger score Excellent (best-in-class for their roles). Worker and tester score Correct (good cost-performance ratio). Benchmarker itself often scores Tune (reasoning too low for model comparison research at flash tier).

    See `.cursor-expert/tutorials/solutions/07-benchmark-guide.md` in the source repo for a complete exemplar.
