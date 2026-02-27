# Exercise 05: Document Use Cases

## Objective

Portfolio exercise. Document 3 AI use cases demonstrating when and why to use multi-agent pipelines.

!!! note "Required Reading"
    - [Foundation README](../index.md) -- "Why multi-agent?" section
    - [Agents | Cursor Learn](https://cursor.com/learn/agents) -- Overview of what agents are and how they work
    - [Working with Agents | Cursor Learn](https://cursor.com/learn/working-with-agents) -- Practical patterns for agent-assisted development
    - [Putting It Together | Cursor Learn](https://cursor.com/learn/putting-it-together) -- End-to-end workflows that demonstrate multi-agent coordination

=== "Cursor"
    The exercises and validation below work in Cursor. Use the Cursor documentation links in Required Reading.

=== "Claude Code"
    The use cases you document here are transferable. Whether using Cursor's subagent dispatch or Claude Code's sequential prompting, the reasoning about *when* and *why* to split work across agents (specialization, safety, cost control) is the same. The agent mapping you define would use the same role names in either system.

## Scenarios

1. **Add pagination to a REST API** (2 files, straightforward)
2. **Migrate a PostgreSQL database schema with zero downtime** (5+ files, cross-cutting)
3. **Add OAuth2 integration with Google and GitHub providers** (6+ files, auth domain, security-critical)

## Task

For each scenario, write:
- **Task description**: What needs to be done (2-3 sentences)
- **Agent mapping**: Which agents handle which parts
- **Artifacts produced**: List the pipeline artifacts that would be created
- **Why multi-agent**: 2-3 sentences explaining why splitting this across agents is better than a single agent

## Output

Write to `.cursor-foundation/tutorials/outputs/05-use-cases.md` with headings `## Use Case 1`, `## Use Case 2`, `## Use Case 3`, each with the 4 subsections above.

!!! success "Validation"
    ```bash
    python3 .cursor-foundation/tutorials/verify.py --exercise 05
    ```

    Checks: 3 use cases present, each has all 4 subsections, "Why multi-agent" sections are at least 20 words.

??? success "Answer"
    This is a portfolio exercise with no single correct answer. A strong response:

    - **Task description**: 2-3 sentences specifying scope, file count, and domains touched
    - **Agent mapping**: Uses correct agent names (jg-subplanner, jg-worker, etc.) and explains what each does for this specific task
    - **Artifacts produced**: Lists all pipeline artifacts including conditional ones (e.g., `debug-diagnosis.json` if tests fail)
    - **Why multi-agent**: Explains the specific benefit for THIS task -- separation of concerns, dedicated review for domain-specific issues, traceable handoffs

    Common mistakes: generic "Why multi-agent" sections that could apply to any task, omitting the debugger from complex scenarios, not distinguishing standard from high-tier agents for security-critical work.

    See `.cursor-foundation/tutorials/solutions/05-use-cases-guide.md` in the source repo for a complete exemplar.
