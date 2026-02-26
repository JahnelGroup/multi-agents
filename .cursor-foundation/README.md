# Foundation Tier

**This tier answers: Can you understand and use AI effectively?**

Think of this as understanding the rules and controls -- you need to know what the parts are and how they work before you get behind the wheel. This tier is for learning, not production. For real projects, copy `.cursor-practitioner/` into your project as `.cursor/`.

## Learning objectives

After reading this, you will understand:
- What coding agents, rules, and pipelines are
- How they work together to turn an issue into a PR
- The vocabulary used throughout the Practitioner and Expert tiers
- Identify when multi-agent is the right approach
- Document AI use cases with agent mappings

## Cursor documentation

Start here for the concepts covered in this tier:

- [Agents | Cursor Learn](https://cursor.com/learn/agents) -- What agents are and how they operate
- [Customizing Agents | Cursor Learn](https://cursor.com/learn/customizing-agents) -- How to define and configure custom agents
- [Working with Agents | Cursor Learn](https://cursor.com/learn/working-with-agents) -- Practical interaction patterns
- [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- `.mdc` rule files and how they activate
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- `SKILL.md` files and on-demand activation
- [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- Agent `.md` frontmatter and AGENTS.md

## What is a `.cursor/` directory?

When you open a project in Cursor, it reads the `.cursor/` directory for three things:

| What | Location | Purpose |
|------|----------|---------|
| **Rules** | `.cursor/rules/*.mdc` | Persistent instructions the AI follows every time (or when triggered). Think of them as team coding standards the AI obeys. |
| **Agents** | `.cursor/agents/*.md` | Role definitions for subagents. Each file defines a name, model, description, and responsibilities. Cursor spawns these as specialized workers. |
| **Skills** | `.cursor/skills/*/SKILL.md` | Reusable instruction sets for specific tasks (e.g. "how to read/write pipeline artifacts"). |

Rules use `.mdc` files with frontmatter:

```yaml
---
description: What this rule does (shown in Cursor UI)
alwaysApply: false
---
# Rule content here
```

`alwaysApply: true` means the AI reads this rule on every prompt. `false` means the AI reads it only when relevant (Cursor matches by description).

Agent definitions use `.md` files with frontmatter:

```yaml
---
name: jg-planner
model: gemini-3.1-pro
description: What this agent does
readonly: true
---
# Agent instructions here
```

See [Customizing agents](https://cursor.com/learn/customizing-agents) and [Cursor Rules documentation](https://docs.cursor.com/context/rules) for full details.

## What is a coding agent?

A coding agent is an AI that uses tools (file editing, search, terminal commands) in a loop to accomplish a goal. You give it a task, and it reads code, makes changes, runs commands, checks results, and iterates until the task is done.

In Cursor, the main AI assistant is already an agent. When you define agent files in `.cursor/agents/`, you create *subagents* -- specialized roles the main agent can delegate to.

See [Agents](https://cursor.com/learn/agents) and [Working with agents](https://cursor.com/learn/working-with-agents) for more.

## What is a pipeline?

A pipeline is a sequence of agents with defined roles that pass work forward. Instead of one agent doing everything, each agent handles one stage:

```
Plan  ->  Implement  ->  Ship
```

Each agent writes a JSON artifact (a result file) that the next agent reads. This creates a traceable record of what happened at each stage.

## Why multi-agent?

A single agent doing everything tends to lose focus: it plans, then implements, then might drift in scope, and it has no built-in way to verify its own work. Splitting responsibilities into specialized roles fixes that:

- **One agent per stage** — Each role has a clear job (plan, implement, ship). The planner doesn't write code; the worker doesn't open PRs. Constraints are more effective than long instructions.
- **Artifacts as handoffs** — Each stage writes a result file the next stage reads. That creates a traceable record and forces explicit handoffs instead of one long, messy context.
- **Structured coordination** — A planner orchestrates the sequence. You don't rely on the model to "figure out" when to test or when to commit; the pipeline defines the order.

The goal of this tier is to understand these ideas so you can explain them — not to run or implement the pipeline yourself. For hands-on use, see Practitioner.

## This pipeline

This Foundation tier uses 3 agents:

```mermaid
graph LR
    A[jg-planner] -->|plan.json| B[jg-worker]
    B -->|worker-result.json| C[jg-git]
    C -->|git-result.json| D[PR ready for review]
```

| Agent | Role | Produces |
|-------|------|----------|
| **jg-planner** | Reads the issue, decides what to build, tells the worker what to do | plan.json |
| **jg-worker** | Edits code, writes tests, reports what changed | worker-result.json |
| **jg-git** | Creates a branch, commits, opens a PR | git-result.json |

One rule ties it together: **jg-planner-first** tells the AI to delegate multi-step work to the planner instead of trying to do everything inline.

## Traced scenario: "Add a health check endpoint"

Here is what happens step by step when you use this pipeline:

### Step 1: You paste a prompt

> "Work on issue #5: Add GET /health endpoint that returns { status: 'ok' }."

Cursor reads your rules, sees `jg-planner-first`, and delegates to jg-planner.

### Step 2: Planner reads the issue and creates a plan

The planner identifies what needs to happen and writes `.pipeline/ISSUE-5/plan.json`:

```json
{
  "affected_files": ["src/routes/health.ts", "src/routes/health.test.ts"],
  "steps": [
    { "order": 1, "file": "src/routes/health.ts", "description": "Create GET /health route returning { status: 'ok' }" },
    { "order": 2, "file": "src/routes/health.test.ts", "description": "Test that GET /health returns 200 with expected body" }
  ]
}
```

### Step 3: Worker implements the plan

The planner dispatches jg-worker with the plan path. The worker reads `plan.json`, creates the files, and writes `.pipeline/ISSUE-5/worker-result.json`:

```json
{
  "status": "completed",
  "files_changed": ["src/routes/health.ts", "src/routes/health.test.ts"],
  "summary": "Created health check endpoint and test"
}
```

### Step 4: Git creates a branch, commits, and opens a PR

The planner dispatches jg-git. Git creates a branch, writes a conventional commit, opens a PR, and writes `.pipeline/ISSUE-5/git-result.json`:

```json
{
  "branch": "feature/issue-5-health-endpoint",
  "commit_sha": "a1b2c3d",
  "pr_url": "https://github.com/org/repo/pull/12"
}
```

You review and merge the PR. Done.

## Self-check: can you talk about it?

After reading this, you should be able to explain the following. Use these as discussion or reflection questions; no implementation required.

- What is the difference between a **rule** and an **agent**? (Rule: persistent instruction the AI obeys. Agent: a role definition the AI can delegate to.)
- What does the **planner** do that the **worker** doesn't? (Planner orchestrates and decides what to build; worker implements code and tests.)
- What is an **artifact** and why do pipelines use them? (A result file one agent writes and another reads; they create traceable handoffs.)
- Why split work across multiple agents instead of one agent doing everything? (Clear roles, explicit handoffs, and structured coordination reduce scope drift and improve verification.)

If you can answer these, you're ready to move on to Practitioner to use and extend the pipeline.

## Glossary

| Term | Definition |
|------|-----------|
| **Agent** | An AI that uses tools in a loop to accomplish a task |
| **Subagent** | A specialized agent spawned by the main agent for a specific role |
| **Rule** | A `.mdc` file that gives the AI persistent instructions |
| **Skill** | A reusable instruction set for a specific task |
| **Artifact** | A JSON file one agent writes and another reads |
| **Pipeline** | A sequence of agents that pass work forward via artifacts |
| **Frontmatter** | YAML metadata at the top of a rule or agent file (between `---` markers) |
| **Acceptance criteria** | Conditions that define when a task is done |
| **State** | A checkpoint of pipeline progress that enables resuming interrupted work |

## Troubleshooting

**Agent didn't pick up my rule**
Check the file is in `.cursor/rules/`, has valid frontmatter (between `---` markers), and the `description` field accurately describes when it should apply. If `alwaysApply` is `false`, the description is how Cursor decides whether to include the rule.

**Model not found**
Some models are hidden by default in Cursor and must be enabled in `Cursor Settings > Models` before agents can use them. Check the `model` field in the agent frontmatter matches an enabled model. If the model isn't available on your plan, substitute any available model. See [Models | Cursor Docs](https://cursor.com/docs/models) for visibility defaults.

**Pipeline artifacts not appearing**
Check `.pipeline/<issue-id>/` exists. The first agent that writes creates it. If you're starting fresh, the planner creates this directory.

## Model fallback

If a model referenced in agent frontmatter isn't available in your Cursor subscription, substitute with any available model. Cheaper models may need more explicit instructions or produce more retries.

## Claude Code

Pipeline concepts (artifacts, agent roles, sequential stages) are the same regardless of IDE. The wiring differs:

| Cursor | Claude Code |
|--------|-------------|
| `.cursor/rules/*.mdc` | `CLAUDE.md` at repo root |
| `.cursor/agents/*.md` | Instructions referenced in `CLAUDE.md` |
| `.cursor/skills/*/SKILL.md` | `.claude/commands/*.md` |
| Subagent dispatch | Sequential prompting through stages |

## Maintenance

These files are derived from the root `.cursor/` bundle. When the bundle is updated, check this directory for changes.

### Tutorials

See `tutorials/` for 5 exercises that test your understanding. These are quiz-style -- read the material, answer questions, produce structured outputs. No code required. See [tutorials/README.md](tutorials/README.md).

### Portfolio

Complete 3 documented AI use cases (exercise 05). For each, describe the task, map it to agents, identify artifacts, and explain why multi-agent beats single-agent.

### Assessment

Demonstrate competency in a conversation with a Practitioner or Expert. You should be able to explain: what agents, rules, and pipelines are; how artifacts create traceable handoffs; and when to split work across agents.

## Next steps

To use this pipeline on a real project with testing, code review, failure handling, and debugging, see `.cursor-practitioner/`.
