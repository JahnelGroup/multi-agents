# Benchmark Review -- Solution Guide

This exercise requires delegation to `jg-benchmarker`. Key evaluation criteria:

## Snapshot (07-benchmark-snapshot.json)

Must include:
- `produced_by: "jg-benchmarker"`
- Per-model entries with benchmark scores (reasoning, coding, instruction_following, speed)
- Pricing data (input/output per 1M tokens)
- Source URLs and retrieval dates for every score
- Models for all agents in the sandbox (gemini-3-flash, gemini-3.1-pro, gpt-5.1-codex-max, gpt-5.3-codex, claude-4.6-sonnet)

## Report (07-benchmark-report.md)

Must include:
- `Produced by: jg-benchmarker` header line
- Agent evaluation table (agent, current model, verdict, key metrics)
- Recommendations for Monitor/Tune/Upgrade verdicts with before/after metrics and cost impact
- Cost impact summary table
- Overall assessment

## What good verdicts look like

- Planner (gemini-3.1-pro): Correct -- adequate reasoning for orchestration
- Subplanner (gpt-5.1-codex-max): Excellent -- best coding/reasoning combo
- Worker (gpt-5.3-codex): Correct -- strong cost-performance ratio
- Tester (gemini-3-flash): Correct -- fast and cheap for structured tasks
- Debugger (claude-4.6-sonnet): Excellent -- best instruction-following
- Git (gemini-3-flash): Correct -- mechanical task, flash sufficient
- Benchmarker (gemini-3-flash): Tune -- reasoning too low for model comparison research
