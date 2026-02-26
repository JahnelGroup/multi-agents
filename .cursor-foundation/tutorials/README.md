# Foundation Tutorials

Quiz-style exercises that test your understanding of multi-agent concepts. No code implementation required.

## Prerequisites

- Read [Foundation README](../README.md) completely
- Python 3.10+ (for verify.py and schema validation)

## Format

Each exercise asks you to read material, answer questions, and write structured outputs to `tutorials/outputs/`. Exercise 04 writes pipeline artifacts to `.pipeline/HEALTH-01/`.

## Exercises

| # | Title | Tests |
|---|-------|-------|
| 01 | [Vocabulary](exercises/01-vocabulary.md) | Define 8 key terms in your own words |
| 02 | [Pattern Recognition](exercises/02-pattern-recognition.md) | Identify agent roles in 4 scenarios |
| 03 | [Artifact Anatomy](exercises/03-artifact-anatomy.md) | Annotate 3 walkthrough artifacts |
| 04 | [Trace Pipeline](exercises/04-trace-pipeline.md) | Produce 3 valid pipeline artifacts |
| 05 | [Document Use Cases](exercises/05-document-use-cases.md) | Portfolio: document 3 AI use cases |

## Verification

```bash
python3 .cursor-foundation/tutorials/verify.py --exercise 01
python3 .cursor-foundation/tutorials/verify.py --all
```

## Claude Code

Exercises use file operations and CLI commands, not Cursor-specific UI. In Claude Code, the same exercises apply -- write the same output files and run the same validation commands.
