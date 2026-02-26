# Exercise 02: Plan a Feature

## Objective

Delegate to the `subplanner` subagent to produce a valid plan.json for the auth middleware feature.

## Required Reading

- [Practitioner walkthrough scenario](../../walkthrough/scenario.md)
- [Pipeline README](../../pipeline/README.md) -- plan.json schema
- [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- How agents break features into plans
- [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- The `jg-pipeline-artifact-io` skill tells the subplanner where to write `plan.json`

> **Claude Code**: The delegation step ("delegate to `jg-subplanner`") uses Cursor's `Task` tool with `subagent_type="jg-subplanner"`. In Claude Code, you would invoke a dedicated prompt with model selection. The resulting `plan.json` artifact and its schema are identical in both systems.

## Context

**Issue #42: Add user authentication middleware**

Acceptance criteria:
1. POST /auth/login accepts email and password, returns a JWT token on success
2. Middleware validates JWT on protected routes, returns 401 if invalid or expired
3. Tests cover valid token, expired token, and missing token scenarios

## Tasks

1. Create directory `sandbox/.pipeline/ISSUE-42/`

2. **Delegate to `jg-subplanner`** with this prompt:
   > Read the issue: "Add user authentication middleware" with these acceptance criteria: [paste ACs above]. The target project is at `sandbox/`. Write `sandbox/.pipeline/ISSUE-42/plan.json` with `affected_files`, `steps`, `acceptance_mapping`, and `"produced_by": "jg-subplanner"`.

   The `produced_by` field is a provenance marker -- it records which agent produced the artifact. The grader checks this to verify delegation actually happened.

3. Verify the plan artifact:
   ```bash
   python3 sandbox/.cursor/pipeline/schema.py --validate sandbox/.pipeline/ISSUE-42/plan.json
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 02
```

Checks: plan.json exists, passes schema validation, has required fields.

## Reflection

- Did the subplanner break the issue into reasonable steps?
- Does the acceptance_mapping correctly link each AC to a test file?
- Would you change anything about the plan before handing it to the worker?
