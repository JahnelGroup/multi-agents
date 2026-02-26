---
name: jg-benchmark-ops
description: "Benchmark collection and evaluation workflow for agent model assignment reviews. Use when pulling benchmarks, evaluating cost/performance, or deciding which models to use for which agents."
---

# JG Benchmark Ops

## When to Trigger

- New model release available for any agent in the project
- User requests benchmark collection, cost/performance evaluation, or model assignment review
- Periodic review (e.g. quarterly) of agent model assignments

## Collection Workflow

1. **Identify sources**
   Use project-defined or common sources: LiveBench, SWE-Bench, Artificial Analysis, or other leaderboards. WebSearch for latest URLs and dates.

2. **Fetch and parse**
   WebFetch for page content. If empty or JS-rendered, use browser MCP or project fallback. Parse into a structured format (YAML/JSON). Record source URL and retrieval date for every score.

3. **Store**
   Write to project-defined path (e.g. `benchmarks/snapshots/YYYY-MM-DD.yaml`). Never overwrite; use new timestamped filename if same-day file exists.

4. **Validate**
   Run project's schema validator (e.g. `python scripts/benchmark_schema.py --validate <path>`) before considering the snapshot complete.

## Evaluation Workflow

- **If the project has an eval script** (e.g. `make benchmark-eval`, `scripts/benchmark_evaluate.py`): run it and read the output. Use its verdicts and metrics in the report.
- **If not**: combine snapshot data with model pricing; for each agent, compare current model to alternatives on primary metrics; assign verdict (Excellent / Correct / Monitor / Tune / Upgrade) and note cost impact.

### Per-Tier Cost Analysis

When evaluating models for a tiered agent setup:

- **Fast tier**: Optimize for cost per token. Acceptable quality threshold: must handle single-file edits and simple tasks without escalation on >80% of trivial tasks.
- **Standard tier**: Balance cost and quality. Compare against fast tier: standard model should reduce retry/escalation rate enough to justify the cost premium.
- **High tier**: Optimize for quality. Acceptable cost threshold: premium is justified if it prevents rework cycles that would cost more in aggregate token spend.

Include a tier cost summary in the evaluation report:

| Tier | Model | Input $/MTok | Output $/MTok | Typical tokens/run | Est. cost/run |
|------|-------|-------------|--------------|-------------------|--------------|
| Fast | ... | ... | ... | ... | ... |
| Standard | ... | ... | ... | ... | ... |
| High | ... | ... | ... | ... | ... |

## Verdict Definitions

| Verdict   | Meaning |
|-----------|--------|
| Excellent | Current model leads its cost tier; no change needed. |
| Correct   | Adequate; within ~5% of tier leader, no cheaper winner. |
| Monitor   | Trails leader by ~5-15% or cheaper option within ~3%; schedule review. |
| Tune      | Same-cost or cheaper model outperforms by >5%; recommend change. |
| Upgrade   | Higher-cost model outperforms on critical-path role; recommend only if cost justified. |

## Cost and Performance

- Use input/output pricing (per token or per MTok) from provider docs or analysis sites.
- Compare: same-tier alternatives (same cost band), cheaper tier, premium tier.
- In recommendations, state: current model, suggested model, metric delta, cost delta.

## Output Expectations

- **Collection**: Sources, dates, snapshot path, list of models collected (and any missing).
- **Evaluation**: Table (Agent | Tier | Model | Verdict | Key metrics); Recommendations (agent, change, before/after, cost impact).
- No agent or rule file updates unless the user explicitly asks to apply recommendations.

## Anti-Patterns

- Do not record scores without source URL and date.
- Do not overwrite existing snapshots.
- Do not apply model assignment changes without explicit approval.
- Do not skip schema validation when the project defines one.
