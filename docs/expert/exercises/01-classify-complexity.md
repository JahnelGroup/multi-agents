# Exercise 01: Classify Complexity

## Objective

Classify 5 task descriptions into trivial/standard/complex tiers, documenting the signals and reasoning for each.

!!! note "Required Reading"
    - [Expert README](../index.md) -- "Complexity classification" section and decision flowchart
    - [Agent Registry](../../reference/agents.md) -- Tier routing table
    - [Custom Agents | Cursor Docs](https://docs.cursor.com/agent/custom-agents) -- How agent definitions and the `model` field control which model runs per role
    - [Rules | Cursor Docs](https://docs.cursor.com/context/rules) -- How `.mdc` rules like `jg-tier-routing.mdc` encode classification logic

=== "Cursor"
    Complexity classification is IDE-agnostic -- the same signals (file count, domain scope, security implications) apply whether you're routing in Cursor subagents or selecting models in Claude Code's sequential prompting. The tier routing table maps directly to model selection parameters.

=== "Claude Code"
    Complexity classification is IDE-agnostic -- the same signals (file count, domain scope, security implications) apply whether you're routing in Cursor subagents or selecting models in Claude Code's sequential prompting. The tier routing table maps directly to model selection parameters.

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
- **agents**: Which tiered agents would handle this (from Agent Registry routing table)

## Output

Write to `tutorials/outputs/01-classifications.json`:

??? example "Expected Output"
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

!!! success "Validation"
    ```bash
    python3 .cursor-expert/tutorials/verify.py --exercise 01
    ```

    Checks: valid JSON, 5 objects, required fields, tier values valid, key classifications match expected tiers.

??? success "Answer"
    | Scenario | Tier | Key Signals |
    |----------|------|-------------|
    | Fix typo in README | **Trivial** | 1 file, docs only, no tests |
    | Add GET /users/:id endpoint | **Standard** | 3 files, single domain, standard CRUD |
    | WebSocket real-time chat | **Complex** | 6+ files, new abstractions, concurrency, rate limiting |
    | Rename UserService to AccountService | **Trivial** | Many files but mechanical, no new logic |
    | Add RBAC with admin/user/guest roles | **Complex** | 4+ files, auth/authz, security-critical, new abstractions |

    The rename (scenario 4) is trivial despite touching many files because it is purely mechanical with no new logic. The RBAC (scenario 5) is complex because auth/authz is security-critical with new middleware abstractions.
