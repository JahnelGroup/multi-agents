# Expert Tier

**This tier answers: Can you architect AI systems and lead others?**

Copy this directory into your project as `.cursor/` for tiered agent routing with cost-optimized model selection.

> For the full course material, exercises, and walkthroughs, see the [Expert docs page](https://jahnelgroup.github.io/multi-agents/expert/).

```bash
cp -r .cursor-expert/* your-project/.cursor/
```

## Quickstart

1. Copy this directory into your project as `.cursor/`
2. Enable the models listed in [AGENTS.md](AGENTS.md) in `Cursor Settings > Models`. See [Models | Cursor Docs](https://cursor.com/docs/models).
3. Create an issue with acceptance criteria
4. Paste this into Cursor:

> "Work on issue #[number]. Classify the task complexity, select the appropriate agent tier, then run the full pipeline: plan, implement, test, review, and ship."

## Agents

15 agents across fast, standard, and high tiers. See [AGENTS.md](AGENTS.md) for the full inventory with tier assignments and I/O mapping.

## Troubleshooting

**worker-fast escalated unexpectedly** -- Normal; escalation is cheap and expected for borderline tasks.

**Cost higher than expected** -- Check the routing log for frequent escalations. Overly aggressive fast-tier assignment causes rework.

**Debugger classified as "escalate" at high tier** -- Review `debug-diagnosis.json` manually; the failure is beyond agent capability.

**Pipeline doesn't resume** -- Check `.pipeline/<issue-id>/state.yaml` exists and has the correct `current_stage`.

**Tiered agent not found** -- Verify the agent file exists in `.cursor/agents/` and the filename matches the planner's routing table.
