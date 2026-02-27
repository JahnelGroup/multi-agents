# Setup Project -- Solution Checklist

## Expected directory structure after setup

```
sandbox/.cursor/
├── agents/
│   ├── jg-planner.md
│   ├── jg-subplanner.md
│   ├── jg-worker.md
│   ├── jg-tester.md
│   ├── jg-reviewer.md
│   ├── jg-debugger.md
│   ├── jg-git.md
│   └── jg-benchmarker.md
├── rules/
│   ├── jg-planner-first.mdc
│   ├── jg-commit-conventions.mdc
│   ├── jg-issue-workflow.mdc
│   └── jg-pr-review.mdc
├── skills/
│   ├── jg-pipeline-artifact-io/SKILL.md
│   └── jg-benchmark-ops/SKILL.md
├── pipeline/
│   ├── schema.py
│   ├── check.py
│   └── README.md
├── templates/
│   ├── agent.md
│   ├── rule.mdc
│   └── state.yaml.example
├── AGENTS.md
└── README.md
```

## Verification commands

All must pass:

```bash
# Agent files exist (at least 7)
ls sandbox/.cursor/agents/*.md | wc -l  # >= 7

# Rule files exist (at least 1)
ls sandbox/.cursor/rules/*.mdc | wc -l  # >= 1

# Pipeline scripts exist
ls sandbox/.cursor/pipeline/schema.py sandbox/.cursor/pipeline/check.py

# Node dependencies installed
ls sandbox/node_modules  # exists

# Tests pass
cd sandbox && npm test  # 1 test, 0 failures

# Typecheck passes
cd sandbox && npm run typecheck  # no errors
```

## Common mistakes

- Copying `docs/practitioner/tutorials/` or `docs/practitioner/walkthrough/` into `.cursor/` (not needed for operations)
- Forgetting to run `npm install` before `npm test`
- Copying from the wrong tier (e.g., Foundation instead of Practitioner)
