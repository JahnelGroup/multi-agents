# multi-agents

Shared multi-agent pipeline setup for Cursor. Provides standard agents, rules, and pipeline tooling that teams copy into their projects. Claude Code support is documented alongside Cursor conventions.

## Prerequisites

- **Cursor** with models enabled for the agents in the pipeline. Some models (e.g. `gpt-5.1-codex-max`) are hidden by default and must be toggled on in `Cursor Settings > Models`. See [Models | Cursor Docs](https://cursor.com/docs/models) for the full list and visibility defaults.
- **Python** 3.10+, **Node.js** 20+, and **git** for tutorials and the sandbox project. See [TESTING.md](TESTING.md) for details.

## Getting started

**Can you explain what agents, rules, and pipelines are?** If not, start with [Foundation](.cursor-foundation/README.md).

**Can you set up a pipeline and build a feature end-to-end?** If not, go to [Practitioner](.cursor-practitioner/README.md).

**Ready to design multi-agent systems and lead others?** See [Expert](.cursor-expert/README.md).

The `.cursor-foundation/`, `.cursor-practitioner/`, and `.cursor-expert/` directories are the canonical source bundles in this repo. Use them for training and for copying into your project.

## Tier directory layout

Each `.cursor-<tier>/` directory follows this structure (not all tiers include every subdirectory):

| Path | Purpose |
|------|---------|
| `agents/*.md` | One file per agent defining its model, role, inputs, outputs, and behavioral instructions. Cursor discovers these as `subagent_type` targets. |
| `rules/*.mdc` | Always-on or file-triggered behavioral guardrails injected into agent context automatically. YAML frontmatter sets `description`, `alwaysApply`, and optional `globs`. |
| `skills/*/SKILL.md` | On-demand capabilities agents pull in when relevant (unlike rules, not auto-injected). Each skill is a subdirectory with a `SKILL.md`. Foundation has none. |
| `pipeline/` | Runtime tooling: `schema.py` (validates artifact JSON), `check.py` (stage-gate invariants), `README.md` (artifact format docs). |
| `templates/` | Scaffolds for new agents, rules, and artifacts. Copy and fill in. Foundation has none. |
| `walkthrough/` | Pre-built example artifacts showing a complete pipeline run. Read-only reference material that ships with the repo. Foundation has none. |
| `tutorials/` | Learner output directory (`outputs/`), solution keys (`solutions/`), and `verify.py` grader. Exercise instructions live in `docs/`. |
| `AGENTS.md` | Agent registry: index table of all agents in the tier, pipeline execution order, and subagent type mappings. |
| `README.md` | Tier landing page: competency question, learning objectives, glossary (Foundation), pipeline flow, and tutorial links. |

## Competency framework

| | Foundation | Practitioner | Expert |
|---|---|---|---|
| **Core Question** | Can you understand and use AI effectively? | Can you build and deploy AI features? | Can you architect AI systems and lead others? |
| **Analogy** | Understanding the rules and controls | Being able to drive anywhere safely | Teaching others to drive and designing better roads |
| **Expectation** | Understand the concept and patterns | Experiment with multi-agent frameworks | Design and deploy multi-agent systems with monitoring |
| **Portfolio** | 3 documented AI use cases | 1 deployed AI use case | 1 client architecture, 1 presentation, 1 mentorship |
| **Assessment** | Conversation with Practitioner or Expert | Technical demo + walk-through with Expert | Peer review + mentorship vouching |
| **Contains** | 3 agents 1 rule 6 exercises | 8 agents 4 rules 2 skills full pipeline 11 exercises | ~15 tiered agents routing rule cost tracking 8 exercises |

## Documentation references

This repo builds on official Cursor and Claude Code documentation:

**Cursor Learn** -- concept guides for working with agents:
- [Agents](https://cursor.com/learn/agents) | [Customizing Agents](https://cursor.com/learn/customizing-agents) | [Working with Agents](https://cursor.com/learn/working-with-agents)
- [Developing Features](https://cursor.com/learn/creating-features) | [Finding and Fixing Bugs](https://cursor.com/learn/finding-and-fixing-bugs) | [Reviewing and Testing Code](https://cursor.com/learn/reviewing-and-testing-code) | [Putting It Together](https://cursor.com/learn/putting-it-together)

**Cursor Docs** -- technical reference:
- [Custom Agents](https://docs.cursor.com/agent/custom-agents) -- agent `.md` files, AGENTS.md, `subagent_type`
- [Rules](https://docs.cursor.com/context/rules) -- `.mdc` rule files, frontmatter, activation
- [Agent Skills](https://docs.cursor.com/context/skills) -- `SKILL.md` format, discovery, on-demand activation

See the [Claude Code](#claude-code) section below for equivalent concepts in that system.

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

Tier directories are canonical in this repo. Update the affected tier directories directly and keep shared files synchronized across tiers when applicable.

Sync checklist:

- Agents shared across tiers: planner, worker, git (Foundation, Practitioner, Expert)
- Agents in Practitioner + Expert: subplanner, tester, reviewer, debugger, benchmarker
- Rules shared: planner-first (all), commit-conventions, issue-workflow, pr-review (Practitioner, Expert)
- Skills shared: pipeline-artifact-io, benchmark-ops (Practitioner, Expert)
- Pipeline: README.md, schema.py, check.py (Practitioner, Expert — Expert extends)
