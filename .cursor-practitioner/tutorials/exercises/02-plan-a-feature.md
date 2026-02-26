# Exercise 02: Plan a Feature

## Objective

Delegate to the `subplanner` subagent to produce a valid plan.json for the auth middleware feature.

## Required Reading

- [Practitioner walkthrough scenario](../../walkthrough/scenario.md)
- [Pipeline README](../../pipeline/README.md) -- plan.json schema
- [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features)

## Context

**Issue #42: Add user authentication middleware**

Acceptance criteria:
1. POST /auth/login accepts email and password, returns a JWT token on success
2. Middleware validates JWT on protected routes, returns 401 if invalid or expired
3. Tests cover valid token, expired token, and missing token scenarios

## Tasks

1. Create directory `sandbox/.pipeline/ISSUE-42/`

2. **Delegate to `jg-subplanner`** with this prompt:
   > Read the issue: "Add user authentication middleware" with these acceptance criteria: [paste ACs above]. The target project is at `sandbox/`. Write `sandbox/.pipeline/ISSUE-42/plan.json` with `affected_files`, `steps`, and `acceptance_mapping`.

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
