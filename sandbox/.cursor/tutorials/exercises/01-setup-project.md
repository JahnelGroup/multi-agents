# Exercise 01: Setup Project

## Objective

Copy the Practitioner tier into the sandbox project as `.cursor/` and verify the full directory structure. Confirms the base project works before starting multi-agent exercises.

## Required Reading

- [Practitioner README](../../README.md)
- [Customizing Agents | Cursor Learn](https://cursor.com/learn/customizing-agents)

## Tasks

1. Copy `.cursor-practitioner/*` into `sandbox/.cursor/`:
   ```bash
   cp -r .cursor-practitioner/* sandbox/.cursor/
   ```

2. Verify directory structure:
   - `sandbox/.cursor/agents/` has agent `.md` files
   - `sandbox/.cursor/rules/` has `.mdc` rule files
   - `sandbox/.cursor/skills/` has skill directories
   - `sandbox/.cursor/pipeline/` has `schema.py` and `check.py`

3. Run commands in the sandbox:
   ```bash
   cd sandbox && npm install
   npm test        # 1 test passes (GET / returns 200)
   npm run typecheck  # no errors
   ```

## Validation

```bash
python3 .cursor-practitioner/tutorials/verify.py --exercise 01
```

Checks: agent files exist, rule files exist, pipeline scripts exist, node_modules exists, npm test passes.

## Reflection

- How many agents are in the Practitioner tier? What are their roles?
- What files does `pipeline/` contain and what do they do?
- Why do we copy the tier into the project rather than referencing it directly?
