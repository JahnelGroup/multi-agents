# Configuration Anatomy -- Solution Guide

This exercise is open-ended but has specific quiz answers. The exemplar in `outputs/06-configuration.md` shows a strong response.

## Quiz Answers

### 1. What three things determine when a rule is applied?

The three frontmatter fields:
- **`alwaysApply`**: If `true`, the rule is injected into every agent context regardless of task
- **`globs`**: File path patterns (e.g., `src/**/*.ts`) that trigger the rule when a matching file is open or being edited
- **`description`**: When `alwaysApply` is `false` and no globs match, Cursor uses the description to decide if the rule is relevant to the current task

### 2. How does a skill differ from a rule in terms of activation?

Rules are **passively injected** -- the system automatically includes them based on `alwaysApply`, `globs`, or description matching. Skills are **actively discovered** -- agents (or Cursor) scan `SKILL.md` description fields and pull in a skill only when its description matches the current task. Rules are pushed; skills are pulled.

### 3. What fields must an agent definition's frontmatter contain at minimum?

- `name` -- identifier used for `subagent_type` dispatch
- `model` -- which AI model to use when spawning the agent
- `description` -- used for discovery and matching

The `readonly` field is important for safety but may be optional depending on the agent's role.

### 4. What role does AGENTS.md play in the pipeline?

AGENTS.md is the pipeline registry: an index table listing all agents, their models, roles, inputs, and outputs. It defines the pipeline execution order (which agent runs in what sequence) and maps role names to `subagent_type` values used in the Task tool. It serves as both human documentation and a reference for orchestrating agents.

## Annotation key points

### Rules annotations should note:
- Frontmatter fields and their values
- Whether `alwaysApply` is true or false and what that means
- Whether `globs` is present or absent
- What the body instructs the AI to do
- When and how the rule would activate

### Skills annotations should note:
- Frontmatter `name` and `description`
- That skills are on-demand, not auto-injected
- The body sections (layout, reading, writing, per-agent mapping, anti-patterns)
- How discovery works via description matching

### Agent annotations should note:
- All 4 frontmatter fields: `name`, `model`, `description`, `readonly`
- The body sections (ROLE, PRIMARY OBJECTIVE, CORE RESPONSIBILITIES, NON-GOALS)
- How AGENTS.md references this agent
