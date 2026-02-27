# Exercise 06: Design Rules & Skills for a Tiered System

## Objective

Design a complete `.cursor/` configuration (rules, skills, agents, AGENTS.md) for the FinSecure system from Exercise 05. This tests your ability to architect the configuration layer that governs a tiered multi-agent pipeline.

!!! note "Required Reading"
    - [Expert README](../index.md) -- Tiered routing, agent inventory
    - [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- `.mdc` format, frontmatter, precedence
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- Official docs on `SKILL.md` format, discovery, and activation
    - [Agent Skills Guide](https://design.dev/guides/claude-skills/) -- Additional guide on SKILL.md format and activation
    - Review the existing tier routing rule: `.cursor-expert/rules/jg-tier-routing.mdc`
    - Review the existing skill: `.cursor/skills/jg-pipeline-artifact-io/SKILL.md`

=== "Cursor"
    The configuration architecture you design here applies to Cursor deployments. Rules live in `.cursor/rules/*.mdc`, skills in `.cursor/skills/*/SKILL.md`, and agent definitions in `.cursor/agents/*.md`.

=== "Claude Code"
    The configuration architecture you design here applies equally to Claude Code deployments. Rules translate to `CLAUDE.md` directives, skills use the identical `.claude/skills/` format, and agent definitions map to model selection in sequential prompting. Design for portability -- the concepts are IDE-agnostic.

## Context

In Exercise 05 you designed an architecture proposal for FinSecure, a fintech platform requiring compliance, security review, and cost monitoring. Now design the `.cursor/` configuration that would implement that architecture's governance layer.

## Tasks

### Part 1: Rules Design

Design 3 project rules (`.mdc` files) for FinSecure. For each rule, specify:
- Filename (e.g. `jg-security-review-required.mdc`)
- Full frontmatter (`description`, `alwaysApply`, `globs` if applicable)
- Body outline: When to Apply, Rule Content, Exempt

Suggested rules:
1. **Tier routing** -- complexity classification and agent assignment (reference `jg-tier-routing.mdc`)
2. **Security review required** -- mandate `jg-reviewer-high` for any file in `src/auth/`, `src/payments/`, or `src/compliance/`
3. **Test coverage threshold** -- block commits if coverage drops below 80%

### Part 2: Skills Design

Design 2 skills (`SKILL.md` files) for FinSecure. For each skill, specify:
- Directory name and SKILL.md frontmatter (`name`, `description`)
- Body sections (when to use, how to execute, output format, anti-patterns)

Suggested skills:
1. **compliance-checker** -- validate that changes comply with financial regulations (SOC2, PCI-DSS)
2. **cost-estimator** -- estimate token/API costs for a pipeline run before execution

### Part 3: Agent Inventory

Create a table of agents for FinSecure, including tiered variants. Show:
- Agent name, model, tier (fast/standard/high), readonly flag
- At least 10 agents covering: planner, subplanner, worker, tester, reviewer, debugger, git, plus domain-specific agents (e.g. `team-security-scanner`, `team-compliance-auditor`)

### Part 4: AGENTS.md Registry

Write the AGENTS.md content that maps pipeline order to agents, including:
- Pipeline execution order (numbered steps)
- Subagent type mapping (which `subagent_type` dispatches to which agent)
- Tier routing table (trivial/standard/complex -> agent variants)

### Part 5: Activation Flow

Create a mermaid diagram showing how rules, skills, and agents interact during a pipeline run. Show:
- When rules are checked (before dispatch, during execution, before commit)
- When skills are loaded (on-demand by description match)
- How agents read rules and skills to modify their behavior

## Output

Write to `tutorials/outputs/06-config-design.md` with these section headings:

```markdown
## Rules Design
(Your 3 rule specifications)

## Skills Design
(Your 2 skill specifications)

## Agent Inventory
(Agent table with tiered variants)

## AGENTS.md Registry
(Pipeline order and subagent mapping)

## Activation Flow
(Mermaid diagram of rule/skill/agent interaction)
```

!!! success "Validation"
    ```bash
    python3 .cursor-expert/tutorials/verify.py --exercise 06
    ```

    Checks: file exists, all 5 sections present, rules section specifies frontmatter fields and 3+ rule names, skills section specifies SKILL.md format and 2+ skills, agent inventory has a table, document includes a mermaid diagram, total document >= 200 words.

??? question "Reflection"
    - How do rules and skills interact? Can a rule reference a skill?
    - What happens if two rules conflict (e.g. one says "always use high tier" and another says "use fast for trivial")?
    - How would you version-control this configuration for a team of 10 developers?

??? success "Answer"
    This is a portfolio exercise requiring 5 sections:

    - **Rules Design**: 3 rules with full frontmatter specs. Key: tier-routing rule, security-review-required rule (with globs for auth/payments/compliance), test-coverage-threshold rule.
    - **Skills Design**: 2 skills with SKILL.md format. Key: compliance-checker and cost-estimator with specific activation descriptions.
    - **Agent Inventory**: 10+ agents with tiered variants and domain-specific agents.
    - **AGENTS.md Registry**: Pipeline order, subagent type mapping, tier routing table.
    - **Activation Flow**: Mermaid diagram showing when rules check (before dispatch, before commit) and when skills load (on-demand).

    See `tutorials/outputs/06-config-design.md` in the source repo for a complete exemplar.
