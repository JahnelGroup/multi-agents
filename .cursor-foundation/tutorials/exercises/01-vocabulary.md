# Exercise 01: Vocabulary

## Objective

Define 9 key terms from the Foundation glossary in your own words. Demonstrates you understand the concepts, not just that you can copy definitions.

## Required Reading

- [Foundation README](../../README.md) -- Glossary section
- [Agents | Cursor Learn](https://cursor.com/learn/agents) -- What agents are and how they operate
- [Customizing Agents | Cursor Learn](https://cursor.com/learn/customizing-agents) -- Defining custom agents, models, and roles
- [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- What rules are (`.mdc` files that give agents persistent instructions)
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- What skills are (`SKILL.md` files that provide reusable capabilities)

> **Claude Code**: These 8 terms are IDE-agnostic. In Claude Code, "agents" map to model prompts, "rules" map to `CLAUDE.md` directives, and "skills" use the same `SKILL.md` format under `.claude/skills/`. Understanding these concepts transfers directly.

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

Write to `tutorials/outputs/01-vocabulary.md`. Use a `## <Term>` heading for each term, followed by a 1-3 sentence definition in your own words.

> **Hint**: The "State" term refers to how pipelines track their progress so work can be resumed if interrupted. Think about what information a pipeline would need to checkpoint and restore.

Do NOT copy the glossary definitions verbatim. Rephrase using your own understanding.

## Validation

```bash
python3 .cursor-foundation/tutorials/verify.py --exercise 01
```

Checks: file exists, all 9 terms have headings, each definition is at least 10 words, no definition is an exact substring of the glossary.
