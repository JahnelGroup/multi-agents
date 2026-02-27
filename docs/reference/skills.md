# Skills

Skills are `SKILL.md` files with YAML frontmatter. They provide specialized capabilities and domain knowledge. Skills are activated on-demand when an agent needs them for a task (e.g. reading pipeline artifacts or running benchmarks).

## Skills Overview

| Name | Description | Available in Tiers |
|------|-------------|--------------------|
| jg-pipeline-artifact-io | Read/write layout for pipeline artifacts in .pipeline/ | Practitioner, Expert |
| jg-benchmark-ops | Benchmark collection and evaluation workflow for agent model assignment reviews | Practitioner, Expert |

## jg-pipeline-artifact-io

**Frontmatter:** `name: jg-pipeline-artifact-io`, `description: "Read/write layout for pipeline artifacts in .pipeline/. Use when any jg- agent reads upstream artifacts or writes its output."`

**Purpose:** Defines the directory layout, reading/writing conventions, and per-agent mapping for pipeline artifacts. Ensures agents pass file paths (not inline content) and validate with schema.py.

**Per-agent mapping:**

| Agent | Reads | Writes |
|-------|-------|--------|
| jg-subplanner | (issue) | plan.json |
| jg-worker | plan.json, debug-diagnosis.json | worker-result.json |
| jg-tester | (runs commands) | test-result.json |
| jg-reviewer | plan.json, worker-result.json | review-result.json |
| jg-debugger | test-result.json, plan.json | debug-diagnosis.json |
| jg-git | (git) | git-result.json |
| jg-planner | all (read-only) | state.yaml if used |

**Expert tier extension:** The Expert version adds **tier tracking fields** that agents must include when writing artifacts:

- **tier_used** (string): "fast" | "standard" | "high"
- **cost_estimate** (string): Human-readable cost estimate
- **escalation_history** (array): For worker-result.json and test-result.json only — `[{ from_tier, to_tier, reason }]`

These fields enable the stage-gate checker to enforce tier routing invariants (e.g. complex tasks must not use fast-tier agents).

## jg-benchmark-ops

**Frontmatter:** `name: jg-benchmark-ops`, `description: "Benchmark collection and evaluation workflow for agent model assignment reviews. Use when pulling benchmarks, evaluating cost/performance, or deciding which models to use for which agents."`

**Purpose:** Guides benchmark collection from sources (LiveBench, SWE-Bench, Artificial Analysis), storage in timestamped snapshots, validation, and evaluation. Produces verdicts (Excellent, Correct, Monitor, Tune, Upgrade) and cost/performance recommendations.

**When to trigger:**

- New model release available for any agent
- User requests benchmark collection or model assignment review
- Periodic review (e.g. quarterly)

**Verdict definitions:**

| Verdict | Meaning |
|---------|---------|
| Excellent | Current model leads its cost tier; no change needed |
| Correct | Adequate; within ~5% of tier leader |
| Monitor | Trails leader by ~5–15%; schedule review |
| Tune | Same-cost or cheaper model outperforms by >5%; recommend change |
| Upgrade | Higher-cost model outperforms on critical-path; recommend if cost justified |

**Anti-patterns:** Do not record scores without source URL and date. Do not overwrite existing snapshots. Do not apply model assignment changes without explicit approval.
