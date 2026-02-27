# Exercise 02: Plan a Feature

## Objective

Delegate to the `subplanner` subagent to produce a valid plan.json for the auth middleware feature.

!!! warning "Delegation Required"
    This exercise **must** use the Task tool with the specified `subagent_type`. Do not write pipeline artifacts manually. The grader cross-references `produced_by` fields and verifies files exist on disk.

!!! note "Required Reading"
    - [Practitioner walkthrough scenario](../walkthrough/scenario.md)
    - [Artifact Schemas](../../reference/artifacts.md) -- plan.json schema
    - [Developing Features | Cursor Learn](https://cursor.com/learn/creating-features) -- How agents break features into plans
    - [Agent Skills | Cursor Docs](https://docs.cursor.com/context/skills) -- The `jg-pipeline-artifact-io` skill tells the subplanner where to write `plan.json`

=== "Cursor"
    The delegation step ("delegate to `jg-subplanner`") uses Cursor's `Task` tool with `subagent_type="jg-subplanner"`.

=== "Claude Code"
    In Claude Code, you would invoke a dedicated prompt with model selection. The resulting `plan.json` artifact and its schema are identical in both systems.

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

!!! success "Validation"
    ```bash
    python3 docs/practitioner/tutorials/verify.py --exercise 02
    ```

    Checks: plan.json exists, passes schema validation, has required fields.

??? question "Reflection"
    - Did the subplanner break the issue into reasonable steps?
    - Does the acceptance_mapping correctly link each AC to a test file?
    - Would you change anything about the plan before handing it to the worker?

??? success "Answer"
    A valid `plan.json` for Issue-42 (auth middleware) should include:

    ```json
    {
      "affected_files": ["src/auth/login.ts", "src/auth/middleware.ts", "src/auth/login.test.ts", "src/auth/middleware.test.ts", "src/app.ts"],
      "steps": [
        { "order": 1, "file": "src/auth/login.ts", "description": "Create POST /auth/login endpoint" },
        { "order": 2, "file": "src/auth/middleware.ts", "description": "Create JWT validation middleware" },
        { "order": 3, "file": "src/auth/login.test.ts", "description": "Write login endpoint tests" },
        { "order": 4, "file": "src/auth/middleware.test.ts", "description": "Write middleware tests" },
        { "order": 5, "file": "src/app.ts", "description": "Register auth routes and middleware" }
      ],
      "acceptance_mapping": { "AC1_login_endpoint": "src/auth/login.test.ts", "AC2_jwt_middleware": "src/auth/middleware.test.ts" },
      "produced_by": "jg-subplanner"
    }
    ```

    Key: every file in `affected_files` must appear in a step. Steps are ordered: implementation before tests.
