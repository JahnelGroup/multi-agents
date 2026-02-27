# Exercise 06: Extend Pipeline

## Objective

Add a new `team-linter` agent to the pipeline. This tests understanding of the agent extension mechanism.

!!! note "Required Reading"
    - [Practitioner README](../index.md) -- "Extending the setup > Add a new agent" section
    - [Customizing Agents | Cursor Learn](https://cursor.com/learn/customizing-agents) -- How to create and register custom agents
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- Agent `.md` frontmatter (name, model, description), AGENTS.md registry format, and `subagent_type` mapping

=== "Cursor"
    Adding a new agent in Cursor uses AGENTS.md with `subagent_type` mapping.

=== "Claude Code"
    In Claude Code, you define the agent's role, model, and responsibilities. The difference is the dispatch mechanism: direct model invocation. The agent definition (role, responsibilities, output schema) is the transferable design artifact.

## Context

The pipeline works end-to-end (Exercises 01-05 complete). Now extend it with a team-specific agent.

## Tasks

1. Copy the agent template:
   ```bash
   cp sandbox/.cursor/templates/agent.md sandbox/.cursor/agents/team-linter.md
   ```

2. Edit `sandbox/.cursor/agents/team-linter.md` frontmatter:
   ```yaml
   ---
   name: team-linter
   model: gemini-3-flash
   description: Runs project linter and writes lint result; use when verifying code style before tests.
   ---
   ```

3. Fill in the body:
   - **ROLE**: Runs the project linter and writes a lint-result.json artifact
   - **CORE RESPONSIBILITIES**: Read plan/worker-result, run `npm run lint`, write `.pipeline/<issue-id>/lint-result.json` with verdict and output
   - **NON-GOALS**: Does not fix lint errors (that's the worker's job)
   - **OUTPUT**: `lint-result.json` with `{ "verdict": "PASS"|"FAIL", "output": "...", "errors": [] }`

4. Add team-linter to `sandbox/.cursor/AGENTS.md`:
   - New row in the agents table
   - Pipeline order note: "2.5. **team-linter** -- After worker; writes `lint-result.json`. On FAIL -> planner re-dispatches worker."
   - Subagent types: add `linter` -> team-linter

!!! success "Validation"
    ```bash
    python3 .cursor-practitioner/tutorials/verify.py --exercise 06
    ```

    Checks: team-linter.md exists with valid frontmatter, AGENTS.md references team-linter and lint-result.json.

??? question "Reflection"
    - How does adding a new agent affect the pipeline flow?
    - What would you need to change in the planner to dispatch to the team-linter?
    - Could this agent be tiered (fast/standard/high)? When would that make sense?
