# Exercise 01: Classify Complexity

## Objective

Classify 5 task descriptions into trivial/standard/complex tiers, documenting the signals and reasoning for each.

## Required Reading

- [Expert README](../../README.md) -- "Complexity classification" section and decision flowchart
- [Expert AGENTS.md](../../AGENTS.md) -- Tier routing table

## Scenarios

1. **"Fix a typo in the README"** -- 1 file, documentation only, no tests needed
2. **"Add a GET /users/:id endpoint with validation and tests"** -- 3 files (route, validation, test), single domain, standard patterns
3. **"Implement WebSocket-based real-time chat with message persistence and rate limiting"** -- 6+ files, new abstractions (WebSocket layer), concurrency, security
4. **"Rename the UserService class to AccountService across the codebase"** -- multiple files but mechanical, no new logic
5. **"Add role-based access control (RBAC) with admin/user/guest roles and middleware"** -- 4+ files, auth/authz domain, security-critical, new abstractions

## Tasks

For each scenario, analyze and document:
- **file_count**: Estimated number of files affected
- **domain_scope**: "single" or "cross-domain"
- **signals**: Factors that drove the classification (from the Expert README flowchart)
- **tier**: "trivial", "standard", or "complex"
- **agents**: Which tiered agents would handle this (from AGENTS.md routing table)

## Output

Write to `tutorials/outputs/01-classifications.json`:

```json
[
  {
    "task": "Fix a typo in the README",
    "file_count": 1,
    "domain_scope": "single",
    "signals": ["single file", "no tests", "documentation only"],
    "tier": "trivial",
    "agents": ["jg-worker-fast", "jg-reviewer-fast"]
  }
]
```

## Validation

```bash
python3 .cursor-expert/tutorials/verify.py --exercise 01
```

Checks: valid JSON, 5 objects, required fields, tier values valid, key classifications match expected tiers.
