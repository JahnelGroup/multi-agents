# Exercise 02: Pattern Recognition

## Objective

Identify which agent role is described in each scenario and what artifact it produces.

!!! note "Required Reading"
    - [Foundation README](../index.md) -- "This pipeline" section and agent table
    - [Working with Agents | Cursor Learn](https://cursor.com/learn/working-with-agents) -- How to interact with and delegate to agents
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- Agent definitions that determine each role's capabilities

=== "Cursor"
    The exercises and validation below work in Cursor. Use the Cursor documentation links in Required Reading.

=== "Claude Code"
    The agent roles (planner, worker, reviewer, debugger, git) and the artifacts they produce are consistent across IDEs. In Claude Code, the same roles would be invoked through sequential prompting rather than Cursor's `Task` tool, but the pattern-matching skills you build here apply directly.

## Scenarios

**Scenario 1**: A developer pastes an issue into Cursor. An agent reads the issue, decides what needs to be built, and tells another agent exactly which files to create and what behavior to implement.

**Scenario 2**: An agent receives a list of files to edit and tests to write. It creates the source files and test files, then reports what it changed.

**Scenario 3**: After code is written, an agent creates a new git branch, writes a commit message that references the issue number, and opens a pull request.

**Scenario 4**: An agent reads a failing test output, inspects the source code, and identifies that line 15 has a comparison operator bug. It classifies this as something the worker can fix.

## Output

Write to `tutorials/outputs/02-patterns.md`. For each scenario, write a `## Scenario N` heading with:
- **Agent**: The agent role name
- **Artifact**: The artifact filename it produces

!!! success "Validation"
    ```bash
    python3 .cursor-foundation/tutorials/verify.py --exercise 02
    ```

    Checks against the answer key. Accepts case-insensitive matches and common variants (e.g., "jg-planner" or "planner").

??? success "Answer"
    **Scenario 1**: Agent = **jg-planner**, Artifact = **plan.json**
    The planner reads the issue and creates an implementation plan.

    **Scenario 2**: Agent = **jg-worker**, Artifact = **worker-result.json**
    The worker implements code and tests per the plan.

    **Scenario 3**: Agent = **jg-git**, Artifact = **git-result.json**
    The git agent creates a branch, commits, and opens a PR.

    **Scenario 4**: Agent = **jg-debugger**, Artifact = **debug-diagnosis.json**
    The debugger diagnoses test failures and classifies the root cause.
