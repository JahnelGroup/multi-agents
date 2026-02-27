# Exercise 01: Vocabulary

## Objective

Define 9 key terms from the Foundation glossary in your own words. Demonstrates you understand the concepts, not just that you can copy definitions.

!!! note "Required Reading"
    - [Foundation README](../index.md) -- Glossary section
    - [Agents | Cursor Learn](https://cursor.com/learn/agents) -- What agents are and how they operate
    - [Customizing Agents | Cursor Learn](https://cursor.com/learn/customizing-agents) -- Defining custom agents, models, and roles
    - [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- What rules are (`.mdc` files that give agents persistent instructions)
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- What skills are (`SKILL.md` files that provide reusable capabilities)

=== "Cursor"
    The exercises and validation below work in Cursor. Use the Cursor documentation links in Required Reading.

=== "Claude Code"
    These 9 terms are IDE-agnostic. In Claude Code, "agents" map to model prompts, "rules" map to `CLAUDE.md` directives, and "skills" use the same `SKILL.md` format under `.claude/skills/`. Understanding these concepts transfers directly.

## Terms to Define

1. Agent
2. Subagent
3. Rule
4. Skill
5. Artifact
6. Pipeline
7. Frontmatter
8. Acceptance criteria
9. State

## Output

Write to `.cursor-foundation/tutorials/outputs/01-vocabulary.md`. Use a `## <Term>` heading for each term, followed by a 1-3 sentence definition in your own words.

!!! tip "Hint"
    The "State" term refers to how pipelines track their progress so work can be resumed if interrupted. Think about what information a pipeline would need to checkpoint and restore.

Do NOT copy the glossary definitions verbatim. Rephrase using your own understanding.

!!! success "Validation"
    ```bash
    python3 .cursor-foundation/tutorials/verify.py --exercise 01
    ```

    Checks: file exists, all 9 terms have headings, each definition is at least 10 words, no definition is an exact substring of the glossary.

??? success "Answer"
    The 9 terms to define, with key points each definition should cover:

    - **Agent**: An AI that uses tools (file editing, search, terminal) in a loop to accomplish a goal. Not just a chatbot -- it takes actions autonomously.
    - **Subagent**: A specialized agent spawned by the main agent for a specific role (e.g., planning, testing). Defined in `.cursor/agents/*.md`.
    - **Rule**: A `.mdc` file in `.cursor/rules/` that gives agents persistent behavioral instructions. Activated by `alwaysApply`, `globs`, or `description` matching.
    - **Skill**: A reusable instruction set (`SKILL.md`) that agents pull in on-demand when the task matches the skill's description. Unlike rules, not auto-injected.
    - **Artifact**: A JSON file one agent writes and another reads. Creates traceable handoffs between pipeline stages (e.g., `plan.json`, `worker-result.json`).
    - **Pipeline**: A sequence of agents that pass work forward via artifacts. Each agent handles one stage (plan, implement, test, review, ship).
    - **Frontmatter**: YAML metadata at the top of a rule or agent file, between `---` markers. Controls activation, model selection, and behavior.
    - **Acceptance criteria**: Conditions that define when a task is done. The plan maps these to implementation steps; the tester verifies them.
    - **State**: A checkpoint of pipeline progress (stored in `state.yaml`) that enables resuming interrupted work without re-running completed stages.

    Your definitions must be in your own words -- the grader rejects verbatim copies of the glossary.
