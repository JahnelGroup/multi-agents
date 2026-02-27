# Understand the Benchmarker -- Solution Guide

This exercise is analytical. The exemplar in `outputs/09-benchmarker-intro.md` shows a strong response. Key points:

## Benchmarker Role

- Primary objective: produce benchmark snapshots and agent-model evaluations for data-driven model assignment decisions
- 4-step execution: Collect (fetch scores) -> Validate (schema check) -> Evaluate (compare assignments) -> Report (per-agent verdicts)
- `readonly: false` but does NOT modify agent files by default -- recommendations are advisory only
- NON-GOALS: does not auto-apply changes, does not run during pipeline (on-demand only)

## Verdict Definitions

| Verdict | Meaning | Action |
|---------|---------|--------|
| Excellent | Current model leads its cost tier on relevant benchmarks | No change |
| Correct | Within ~5% of tier leader, no cheaper alternative wins | No change; monitor |
| Monitor | Trails by ~5-15%, or a cheaper option is within ~3% | Schedule review soon |
| Tune | A same-cost or cheaper model outperforms by >5% | Switch to better-value model |
| Upgrade | A higher-cost model significantly outperforms on a critical role | Upgrade if cost justifiable |

## Per-Agent Focus

- Planner needs reasoning (not coding) because it orchestrates, not implements
- Worker needs coding/SWE benchmarks because it writes code
- Reviewer needs language quality and global knowledge for precise written feedback
- Tester needs instruction-following to run commands exactly as specified
- Debugger needs reasoning + coding to trace root causes
- Git needs only instruction-following (mechanical task)

## When to Review

Three triggers: new model release, quarterly cadence, performance regression. The benchmarker doesn't auto-apply because model changes affect cost, quality, and pipeline behavior -- humans make the final decision.
