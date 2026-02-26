# Exercise 03: Artifact Anatomy

## Objective

Read 3 real walkthrough artifacts from the Practitioner tier and annotate each.

## Required Reading

- [Pipeline README](../../.cursor-practitioner/pipeline/README.md) -- artifact schemas
- Practitioner walkthrough artifacts:
  - `.cursor-practitioner/walkthrough/plan.json`
  - `.cursor-practitioner/walkthrough/worker-result.json`
  - `.cursor-practitioner/walkthrough/debug-diagnosis.json`

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
