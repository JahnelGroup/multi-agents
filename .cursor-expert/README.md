# Expert Tier

**This tier answers: Can you architect AI systems and lead others?**

Like teaching others to drive and designing better roads -- you understand the system well enough to improve it and help others navigate it.

Copy this directory into your project as `.cursor/` for tiered agent routing with cost-optimized model selection.

```bash
cp -r .cursor-expert/* your-project/.cursor/
```

## Quickstart

1. Copy this directory into your project as `.cursor/`
2. Enable the models listed in `AGENTS.md` in `Cursor Settings > Models`. Some models (e.g. `gpt-5.1-codex-max`) are hidden by default. See [Models | Cursor Docs](https://cursor.com/docs/models).
3. Create an issue with acceptance criteria
4. Paste this into Cursor:

> "Work on issue #[number]. Classify the task complexity, select the appropriate agent tier, then run the full pipeline: plan, implement, test, review, and ship."

## Agents (15 total)

See [AGENTS.md](AGENTS.md) for the full index with tier assignments and I/O mapping.

| Agent | Tier | Role |
|-------|------|------|
| jg-planner | -- | Orchestrates pipeline, classifies complexity, routes to tiers |
| jg-subplanner | Standard | Decomposes issues into ordered plans |
| jg-subplanner-high | High | Plans with dependency graphs and risk analysis |
| jg-worker-fast | Fast | Single-file edits; escalates if exceeds scope |
| jg-worker | Standard | Multi-file implementation |
| jg-worker-high | High | Complex features with risk assessment |
| jg-tester-fast | Fast | Phase 1 only (lint, typecheck, unit tests) |
| jg-tester | Standard | Phase 1 + Phase 2 verification |
| jg-reviewer-fast | Fast | Scope check and lint-level review |
| jg-reviewer | Standard | Full quality gate |
| jg-reviewer-high | High | Architecture and security review |
| jg-debugger | Standard | Failure classification and diagnosis |
| jg-debugger-high | High | Multi-causal, cross-module analysis |
| jg-git | -- | Branch, commit, PR |
| jg-benchmarker | -- | Model cost/performance evaluation |

## Model fallbacks

| Agent | Default | Fallback |
|-------|---------|----------|
| jg-planner | gemini-3.1-pro | Any reasoning model |
| jg-subplanner[-high] | gpt-5.1-codex-max | Any code-capable model |
| jg-worker-fast | gemini-3-flash | Any fast model |
| jg-worker | gpt-5.3-codex | Any code-capable model |
| jg-worker-high | gpt-5.1-codex-max | Any code-capable model |
| jg-tester[-fast] | gemini-3-flash | Any fast model |
| jg-reviewer[-fast] | gemini-3-flash | Any fast model |
| jg-reviewer[-high] | gemini-3.1-pro | Any reasoning model |
| jg-debugger | claude-4.6-sonnet | Any reasoning model |
| jg-debugger-high | claude-opus-4.6 | Any reasoning model |
| jg-git | gemini-3-flash | Any fast model |
| jg-benchmarker | gemini-3-flash | Any fast model |

## Troubleshooting

**worker-fast escalated unexpectedly**
The task was more complex than the initial classification suggested. This is normal -- escalation is cheap and expected for borderline tasks.

**Cost higher than expected**
Check the routing log for frequent escalations. If most tasks escalate, your classification criteria may be too aggressive about assigning the fast tier.

**Debugger classified as "escalate" at high tier**
The failure is genuinely beyond agent capability. Review the `debug-diagnosis.json` manually.

**Pipeline doesn't resume**
Check `.pipeline/<issue-id>/state.yaml` exists and has the correct `current_stage`. If missing, the planner starts from scratch.

**Tiered agent not found**
Verify the agent file exists in `.cursor/agents/` and the filename in the planner's routing table matches exactly.

## Claude Code

Pipeline concepts (artifacts, roles, stage gates, tiered routing) are IDE-agnostic. Tiered agent dispatch is Cursor-specific (subagent architecture). In Claude Code, implement tier routing as sequential prompting with model selection:

| Cursor | Claude Code |
|--------|-------------|
| `.cursor/rules/*.mdc` | `CLAUDE.md` at repo root |
| `.cursor/agents/*.md` | Referenced docs in `CLAUDE.md` |
| `.cursor/skills/*/SKILL.md` | `.claude/commands/*.md` |
| `subagent_type` dispatch with tier | Model selection per prompt |
| `jg-tier-routing.mdc` | Routing logic in `CLAUDE.md` |

Walkthrough content and pipeline artifacts work in both environments.
