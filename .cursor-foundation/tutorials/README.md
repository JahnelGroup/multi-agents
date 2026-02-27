# Foundation Tutorials

Quiz-style exercises that test your understanding of multi-agent concepts. No code implementation required.

## Prerequisites

- Read [Foundation README](../README.md) completely
- Python 3.10+ (for verify.py and schema validation)

## Cursor Documentation

These exercises build on concepts covered in the official Cursor documentation:

| Topic | Link | Exercises |
|-------|------|-----------|
| What agents are | [Agents - Cursor Learn](https://cursor.com/learn/agents) | 01, 02 |
| Agent customization | [Customizing Agents - Cursor Learn](https://cursor.com/learn/customizing-agents) | 01 |
| Working with agents | [Working with Agents - Cursor Learn](https://cursor.com/learn/working-with-agents) | 02 |
| Feature development | [Developing Features - Cursor Learn](https://cursor.com/learn/creating-features) | 03, 04 |
| End-to-end workflows | [Putting It Together - Cursor Learn](https://cursor.com/learn/putting-it-together) | 04, 05 |
| Rules (.mdc) | [Rules - Cursor Docs](https://docs.cursor.com/context/rules) | 06 |
| Skills (SKILL.md) | [Agent Skills - Cursor Docs](https://docs.cursor.com/context/skills) | 06 |
| Custom agents | [Custom Agents - Cursor Docs](https://docs.cursor.com/agent/custom-agents) | 06 |

## Format

Each exercise asks you to read material, answer questions, and write structured outputs to `tutorials/outputs/`. Exercise 04 writes pipeline artifacts to `.pipeline/HEALTH-01/`.

## Exercises

| # | Title | Tests |
|---|-------|-------|
| 01 | [Vocabulary](../../docs/foundation/exercises/01-vocabulary.md) | Define 9 key terms in your own words |
| 02 | [Pattern Recognition](../../docs/foundation/exercises/02-pattern-recognition.md) | Identify agent roles in 4 scenarios |
| 03 | [Artifact Anatomy](../../docs/foundation/exercises/03-artifact-anatomy.md) | Annotate 3 walkthrough artifacts |
| 04 | [Trace Pipeline](../../docs/foundation/exercises/04-trace-pipeline.md) | Produce 3 valid pipeline artifacts |
| 05 | [Document Use Cases](../../docs/foundation/exercises/05-document-use-cases.md) | Portfolio: document 3 AI use cases |
| 06 | [Configuration Anatomy](../../docs/foundation/exercises/06-configuration-anatomy.md) | Annotate rules, skills & agent files; quiz |

## Verification

```bash
python3 .cursor-foundation/tutorials/verify.py --exercise 01   # single exercise
python3 .cursor-foundation/tutorials/verify.py --all          # all 6 exercises
```

## Claude Code

Exercises use file operations and CLI commands, not Cursor-specific UI. In Claude Code, the same exercises apply -- write the same output files and run the same validation commands.
