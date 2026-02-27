# Getting Started: Adopt the Pipeline

!!! note "Prerequisites"
    - Cursor installed with agent models enabled
    - Python 3.10+, Node.js 20+, git
    - Models enabled: `gemini-3.1-pro`, `gpt-5.3-codex`, `gpt-5.1-codex-max`, `gemini-3-flash`, `claude-4.6-sonnet` (check Cursor Settings > Models)

## Choose your tier

- **Most teams**: Start with **Practitioner** (8 agents, full pipeline)
- **Advanced teams with cost concerns**: Use **Expert** (tiered routing, ~15 agents)
- **New to AI agents**: Read **Foundation** first (concepts only)

## Copy into your project

```bash
cp -r .cursor-practitioner/* your-project/.cursor/
```

## Customize for your team

- Use `team-` prefix for team-specific agents/rules
- Keep `jg-` files as read-only upstream references
- Diff before overwriting if you've modified any `jg-` files

## Run your first real issue

1. Create or pick an issue in your project
2. Paste in Cursor: "Work on issue #N: [description]"
3. The `jg-planner-first` rule triggers automatic delegation
4. Watch the pipeline: planner → subplanner → worker → tester → reviewer → git
5. Review the generated PR

## What "done" looks like

The pipeline produces a PR with conventional commits, passing tests, and a review-result. A human reviews and merges.

## Upgrading tiers

- Copy the new tier directory over `.cursor/`
- Keep `team-` prefixed files (they survive upgrades)
- Diff before overwriting modified `jg-` files

## Troubleshooting

!!! warning "Agent didn't pick up rule"
    Check frontmatter, `description` field, and file location. The file must be in `.cursor/rules/`, have valid frontmatter (between `---` markers), and the `description` field must accurately describe when it should apply.

!!! warning "Model not found"
    Enable the model in Cursor Settings > Models. Some models are hidden by default and must be enabled before agents can use them.

!!! warning "Pipeline artifacts not appearing"
    The first agent creates `.pipeline/<issue-id>/`. If you're starting fresh, the planner creates this directory.
