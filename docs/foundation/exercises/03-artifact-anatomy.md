# Exercise 03: Artifact Anatomy

## Objective

Read 3 real walkthrough artifacts from the Practitioner tier and annotate each.

!!! note "Required Reading"
    - [Artifact Schemas](../../reference/artifacts.md) -- pipeline artifact schemas
    - Practitioner walkthrough artifacts:
      - `docs/practitioner/walkthrough/plan.json`
      - `docs/practitioner/walkthrough/worker-result.json`
      - `docs/practitioner/walkthrough/debug-diagnosis.json`
    - [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- How agents produce artifacts during feature development
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How agent definitions determine which agent writes which artifact

=== "Cursor"
    The exercises and validation below work in Cursor. Use the Cursor documentation links in Required Reading.

=== "Claude Code"
    Pipeline artifacts (plan.json, worker-result.json, debug-diagnosis.json) are IDE-agnostic JSON files. The same schemas and writer/consumer relationships apply in Claude Code workflows -- the artifact format is the portable unit of multi-agent coordination.

## Task

For each artifact, document:
- **Writer**: Which agent produces this artifact
- **Required fields**: List the required keys per the pipeline schema
- **Consumer**: Which agent reads this artifact next, and what it uses from it

## Output

Write to `docs/foundation/tutorials/outputs/03-annotations.md` with headings `## plan.json`, `## worker-result.json`, `## debug-diagnosis.json`, each containing Writer, Required fields, and Consumer subsections.

!!! success "Validation"
    ```bash
    python3 docs/foundation/tutorials/verify.py --exercise 03
    ```

    Checks: file exists, 3 artifact sections present, each has Writer/Required fields/Consumer subsections, Writer values match expected agents.

??? success "Answer"
    **plan.json**

    - Writer: jg-subplanner
    - Required fields: `affected_files`, `steps`, `acceptance_mapping`
    - Consumer: jg-worker (reads steps and affected_files to know what to implement)

    **worker-result.json**

    - Writer: jg-worker
    - Required fields: `status`, `files_changed`, `blockers`, `summary`
    - Consumer: jg-tester (reads to know what changed, then runs tests)

    **debug-diagnosis.json**

    - Writer: jg-debugger
    - Required fields: `failure_source`, `failure_description`, `root_cause`, `root_cause_file`, `root_cause_line`, `classification`
    - Consumer: jg-worker (reads root_cause and fix_instructions to apply the fix)
