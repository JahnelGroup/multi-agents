# Exercise 02: Pattern Recognition

## Objective

Identify which agent role is described in each scenario and what artifact it produces.

## Required Reading

- [Foundation README](../../README.md) -- "This pipeline" section and agent table
- [Working with Agents | Cursor Learn](https://cursor.com/learn/working-with-agents)

## Scenarios

**Scenario 1**: A developer pastes an issue into Cursor. An agent reads the issue, decides what needs to be built, and tells another agent exactly which files to create and what behavior to implement.

**Scenario 2**: An agent receives a list of files to edit and tests to write. It creates the source files and test files, then reports what it changed.

**Scenario 3**: After code is written, an agent creates a new git branch, writes a commit message that references the issue number, and opens a pull request.

**Scenario 4**: An agent reads a failing test output, inspects the source code, and identifies that line 15 has a comparison operator bug. It classifies this as something the worker can fix.

## Output

Write to `tutorials/outputs/02-patterns.md`. For each scenario, write a `## Scenario N` heading with:
- **Agent**: The agent role name
- **Artifact**: The artifact filename it produces

## Validation

```bash
python3 .cursor-foundation/tutorials/verify.py --exercise 02
```

Checks against the answer key. Accepts case-insensitive matches and common variants (e.g., "jg-planner" or "planner").
