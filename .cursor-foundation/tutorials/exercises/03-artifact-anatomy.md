# Exercise 03: Artifact Anatomy

## Objective

Read 3 real walkthrough artifacts from the Practitioner tier and annotate each.

## Required Reading

- [Pipeline README](../../.cursor-practitioner/pipeline/README.md) -- artifact schemas
- Practitioner walkthrough artifacts:
  - `.cursor-practitioner/walkthrough/plan.json`
  - `.cursor-practitioner/walkthrough/worker-result.json`
  - `.cursor-practitioner/walkthrough/debug-diagnosis.json`
- [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- How agents produce artifacts during feature development
- [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How agent definitions determine which agent writes which artifact

> **Claude Code**: Pipeline artifacts (plan.json, worker-result.json, debug-diagnosis.json) are IDE-agnostic JSON files. The same schemas and writer/consumer relationships apply in Claude Code workflows -- the artifact format is the portable unit of multi-agent coordination.

## Task

For each artifact, document:
- **Writer**: Which agent produces this artifact
- **Required fields**: List the required keys per the pipeline schema
- **Consumer**: Which agent reads this artifact next, and what it uses from it

## Output

Write to `tutorials/outputs/03-annotations.md` with headings `## plan.json`, `## worker-result.json`, `## debug-diagnosis.json`, each containing Writer, Required fields, and Consumer subsections.

## Validation

```bash
python3 .cursor-foundation/tutorials/verify.py --exercise 03
```

Checks: file exists, 3 artifact sections present, each has Writer/Required fields/Consumer subsections, Writer values match expected agents.
