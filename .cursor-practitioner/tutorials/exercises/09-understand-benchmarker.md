# Exercise 09: Understand the Benchmarker

## Objective

Understand the `jg-benchmarker` support agent and the `jg-benchmark-ops` skill. Learn how cost vs performance evaluation works, when to trigger a review, and how to interpret the 5 verdict levels. This prepares you for Expert-level benchmark execution.

## Required Reading

- `sandbox/.cursor/agents/jg-benchmarker.md` -- Role, execution style, per-agent benchmark focus table
- `sandbox/.cursor/skills/jg-benchmark-ops/SKILL.md` -- Collection/evaluation workflow, verdict definitions, anti-patterns
- `sandbox/.cursor/AGENTS.md` -- Where the benchmarker sits in the agent registry (support, not pipeline)
- [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How the `model` field in agent frontmatter determines which model an agent uses
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- How skills like `jg-benchmark-ops` activate on-demand via description matching
- [Agent Skills Guide](https://design.dev/guides/claude-skills/) -- Additional guide on skill format and discovery

> **Claude Code**: The same concepts apply to Claude Code. Model selection in Claude Code is done via model parameters in sequential prompting. The benchmarker workflow (collect -> evaluate -> recommend) is IDE-agnostic -- you would run the same evaluation regardless of whether your agents live in `.cursor/agents/` or are invoked through Claude's API.

## Context

As models evolve rapidly (new releases, price changes, capability improvements), agent model assignments can become stale. The benchmarker is a support agent that helps you keep assignments optimal without manual research. Unlike pipeline agents (planner, worker, tester, etc.), the benchmarker runs **on-demand** and is **advisory only** -- it never modifies agent files without explicit approval.

## Tasks

### Part 1: Benchmarker Role

Read `sandbox/.cursor/agents/jg-benchmarker.md`. Identify and summarize:
- The agent's primary objective (one sentence)
- The 4-step execution style: Collect -> Validate -> Evaluate -> Report
- Why the benchmarker is `readonly: false` but still does not modify agent files by default
- What the NON-GOALS section says about its boundaries

### Part 2: Verdict Definitions

Read `sandbox/.cursor/skills/jg-benchmark-ops/SKILL.md`. For each of the 5 verdicts, explain:
- **Excellent**: What it means and what action to take
- **Correct**: What it means and what action to take
- **Monitor**: What it means and what action to take
- **Tune**: What it means and what action to take
- **Upgrade**: What it means and what action to take

### Part 3: Per-Agent Benchmark Focus

Read the per-agent benchmark focus table in the benchmarker agent file. Explain:
- Why does the planner need strong reasoning scores but not coding scores?
- Why does the worker prioritize coding and SWE benchmarks?
- Why does the reviewer need language and global benchmarks?
- Pick one additional agent and explain its benchmark focus

### Part 4: When to Review

Answer these questions in your own words:
1. What are the 3 triggers for a benchmark review? (new model release, quarterly cadence, performance regression)
2. Why does the benchmarker not apply model changes by default?
3. How would you check if your sandbox agents are using optimal models today?
4. What would happen if you never ran a benchmark review?

## Output

Write to `tutorials/outputs/09-benchmarker-intro.md` with these section headings:

```markdown
## Benchmarker Role
(Your summary of the agent's purpose and execution style)

## Verdict Definitions
(All 5 verdicts with explanations)

## Per-Agent Focus
(Why different agents need different benchmarks)

## When to Review
(Your answers to the 4 questions)
```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 09
```

Checks: file exists, all 4 sections present, verdict section mentions all 5 verdicts, per-agent focus mentions 3+ agent roles, when-to-review section has sufficient depth.

## Reflection

- If a cheaper model scores within 3% of the current model on all relevant benchmarks, should you switch? What factors beyond benchmark scores matter?
- How does the benchmarker relate to the cost analysis you'll do in Expert exercises?
- Could the benchmarker itself be assigned to a cheaper model? What benchmarks would it need?
