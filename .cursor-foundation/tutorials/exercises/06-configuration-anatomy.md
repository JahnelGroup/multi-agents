# Exercise 06: Rules, Skills & Agent Configuration

## Objective

Read and annotate the three configuration primitives that control AI agent behavior: **rules** (`.mdc`), **skills** (`SKILL.md`), and **agent definitions** (`.md`). Demonstrate you understand each format's frontmatter, purpose, and when it activates.

## Required Reading

- [Foundation README](../../README.md) -- Glossary (terms: rule, skill, agent, frontmatter)
- [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- `.mdc` format, frontmatter fields, precedence hierarchy
- [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- Agent `.md` format, AGENTS.md registry
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- Official docs on `SKILL.md` format, discovery, and activation
- [Agent Skills Guide](https://design.dev/guides/claude-skills/) -- Additional guide on SKILL.md format and dynamic context discovery

> **Claude Code**: Claude Code uses an equivalent system. Rules map to `CLAUDE.md` project instructions. Skills use the identical `.claude/skills/` directory with the same `SKILL.md` format. Agent definitions are handled via sequential prompting with model selection. The concepts below apply to both; only file paths differ.

## Context

You defined these terms in Exercise 01. Now you will read the actual files, annotate their structure, and answer conceptual questions about when each activates and how they interact.

## Tasks

### Part 1: Annotate Rules

Read these two rule files:
- `.cursor-foundation/rules/jg-planner-first.mdc` (or the parent `.cursor/rules/jg-planner-first.mdc`)
- Any other `.mdc` rule in the repo (e.g. `.cursor/rules/jg-issue-workflow.mdc`)

For each rule, note:
- The **frontmatter fields**: `description`, `alwaysApply`, `globs` (which may be absent)
- The **body sections** and what each instructs the AI to do
- When this rule would be activated (based on `alwaysApply` and `globs`)

### Part 2: Annotate a Skill

Read this skill file:
- `.cursor/skills/jg-pipeline-artifact-io/SKILL.md`

Note:
- The **frontmatter fields**: `name`, `description`
- The **body sections** (directory layout, reading, writing, per-agent mapping, anti-patterns)
- How the skill is discovered and activated (by description match when the agent's task is relevant)

### Part 3: Annotate an Agent

Read this agent definition:
- `.cursor-foundation/agents/jg-planner.md`

Note:
- The **frontmatter fields**: `name`, `model`, `description`, `readonly`
- The **body sections** (ROLE, PRIMARY OBJECTIVE, CORE RESPONSIBILITIES, NON-GOALS)
- How AGENTS.md references this agent in the pipeline order

### Part 4: Quiz Questions

Answer these questions in your own words (1-3 sentences each):

1. What three things determine when a rule is applied? (Hint: frontmatter fields)
2. How does a skill differ from a rule in terms of activation?
3. What fields must an agent definition's frontmatter contain at minimum?
4. What role does AGENTS.md play in the pipeline?

## Output

Write to `tutorials/outputs/06-configuration.md`. Use these section headings:

```markdown
## Rules
(Your annotations of the two rule files)

## Skills
(Your annotation of the skill file)

## Agents
(Your annotation of the agent file)

## Quiz Answers
(Your answers to the 4 questions)
```

## Validation

```bash
python3 .cursor-foundation/tutorials/verify.py --exercise 06
```

Checks: file exists, all 4 sections present, each section mentions the correct frontmatter fields, quiz answers have sufficient depth.
