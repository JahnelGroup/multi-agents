# multi-agents

Shared multi-agent pipeline setup for Cursor. Provides standard agents, rules, and pipeline tooling that teams copy into their projects. Claude Code support is documented alongside Cursor conventions.

## Getting started

**Can you explain what agents, rules, and pipelines are?** If not, start with [Foundation](.cursor-foundation/README.md).

**Can you set up a pipeline and build a feature end-to-end?** If not, go to [Practitioner](.cursor-practitioner/README.md).

**Ready to design multi-agent systems and lead others?** See [Expert](.cursor-expert/README.md).

The root `.cursor/` directory is the canonical source bundle. The `.cursor-foundation/`, `.cursor-practitioner/`, and `.cursor-expert/` directories are the structured learning and adoption points — use them for training and for copying into your project.

## Competency framework

| | Foundation | Practitioner | Expert |
|---|---|---|---|
| **Core Question** | Can you understand and use AI effectively? | Can you build and deploy AI features? | Can you architect AI systems and lead others? |
| **Analogy** | Understanding the rules and controls | Being able to drive anywhere safely | Teaching others to drive and designing better roads |
| **Expectation** | Understand the concept and patterns | Experiment with multi-agent frameworks | Design and deploy multi-agent systems with monitoring |
| **Portfolio** | 3 documented AI use cases | 1 deployed AI use case | 1 client architecture, 1 presentation, 1 mentorship |
| **Assessment** | Conversation with Practitioner or Expert | Technical demo + walk-through with Expert | Peer review + mentorship vouching |
| **Contains** | 3 agents 1 rule | 8 agents 4 rules 2 skills full pipeline | ~15 tiered agents routing rule cost tracking |

## Adoption

Copy `.cursor-<tier>/` into your project as `.cursor/`. Most teams should start with **Practitioner**.

```bash
cp -r .cursor-practitioner/* your-project/.cursor/
```

## Tutorials

Each tier includes a `tutorials/` directory with exercises. Foundation exercises are quiz-based and conceptual. Practitioner exercises are hands-on and require delegating to subagents. Expert exercises involve tiered routing, cost analysis, and architecture design. See [TESTING.md](TESTING.md) for the full test plan.

## Upgrading tiers

- Copy `.cursor-practitioner/` (or expert) over your `.cursor/`
- Keep `jg-` files as read-only upstream references
- Put customizations in `team-` or `my-` prefixed files so they survive upgrades
- Diff before overwriting if you've modified any `jg-` files

## Naming convention

| Prefix | Meaning |
|--------|---------|
| `jg-*` | Shared bundle — do not modify in your project |
| `<team>-*` | Team or project conventions |
| Unmarked | Individual developer additions |

## Claude Code

Pipeline concepts (artifacts, agent roles, stage gates) are IDE-agnostic. The wiring differs:

| Cursor | Claude Code |
|--------|-------------|
| `.cursor/rules/*.mdc` | `CLAUDE.md` at repo root |
| `.cursor/agents/*.md` | Referenced docs in `CLAUDE.md` |
| `.cursor/skills/*/SKILL.md` | `.claude/commands/*.md` |
| `subagent_type` dispatch | Sequential prompting through stages |

Walkthrough content and pipeline artifacts work in both environments.

## Security and guardrails

- Agents that can write code: worker, debugger
- Agents that can run commands: tester, git
- Agents that cannot: merge PRs, force push, skip hooks, push to main
- `readonly: true` on planner, reviewer, subplanner
- Always review agent-generated PRs before merging

## .gitignore

`.pipeline/` is runtime state — do not commit. Walkthrough artifacts in tier directories live under `walkthrough/`, not `.pipeline/`, so they ship with the repo.

## Cost awareness

Each pipeline run invokes multiple AI models. See Expert tier for detailed cost analysis and tiered model strategies.

## Migration from .cursor-jg

If your project previously used `.cursor-jg/` references, replace all paths with `.cursor/`. The old path convention is retired.

## Versioning

`VERSION` file at repo root (semver). Bumped on any change to agents, rules, skills, or pipeline.

## Maintenance policy

Root `.cursor/` is the canonical source. Tier directories are derived from it. Update `.cursor/` first, then propagate.

Sync checklist:

- Agents shared across tiers: planner, worker, git (Foundation, Practitioner, Expert)
- Agents in Practitioner + Expert: subplanner, tester, reviewer, debugger, benchmarker
- Rules shared: planner-first (all), commit-conventions, issue-workflow, pr-review (Practitioner, Expert)
- Skills shared: pipeline-artifact-io, benchmark-ops (Practitioner, Expert)
- Pipeline: README.md, schema.py, check.py (Practitioner, Expert — Expert extends)
