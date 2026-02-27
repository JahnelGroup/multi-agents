# Foundation Tier

**This tier answers: Can you understand and use AI effectively?**

This tier is for learning, not production. For real projects, copy `.cursor-practitioner/` into your project as `.cursor/`.

> For the full course material, exercises, and walkthroughs, see the [Foundation docs page](https://jahnelgroup.github.io/multi-agents/foundation/).

## This pipeline

This Foundation tier uses 3 agents:

```mermaid
graph LR
    A[jg-planner] -->|plan.json| B[jg-worker]
    B -->|worker-result.json| C[jg-git]
    C -->|git-result.json| D[PR ready for review]
```

## Troubleshooting

**Agent didn't pick up my rule** -- Check the file is in `.cursor/rules/` with valid frontmatter and an accurate `description` field.

**Model not found** -- Enable the model in `Cursor Settings > Models`. See [Models | Cursor Docs](https://cursor.com/docs/models).

**Pipeline artifacts not appearing** -- Check `.pipeline/<issue-id>/` exists. The planner creates this directory.
