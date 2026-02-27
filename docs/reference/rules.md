# Rules

Rules are `.mdc` files with YAML frontmatter. They define behavior for agents: `alwaysApply: true` rules run on every request; `alwaysApply: false` rules are applied when relevant to the task.

## Rules Overview

| Name | alwaysApply | Description | Available in Tiers |
|------|-------------|-------------|--------------------|
| jg-planner-first | true | Delegate multi-step work to jg-planner first | Foundation, Practitioner, Expert |
| jg-commit-conventions | false | Commit and PR conventions | Practitioner, Expert |
| jg-issue-workflow | false | Issue-as-source-of-truth and start/completion workflow | Practitioner, Expert |
| jg-pr-review | false | PR review categories and decision rules | Practitioner, Expert |
| jg-tier-routing | true | Complexity classification and tiered agent routing | Expert only |

## jg-planner-first

**Frontmatter:** `description: Delegate multi-step work to jg-planner first`, `alwaysApply: true`

**Purpose:** Ensures multi-step implementation requests are routed through the planner instead of being executed directly. Single-file edits and factual questions are exempt.

??? note "Key sections"
    **Pre-Action Gate (MANDATORY)**

    Before any Write, StrReplace, or Task call: classify the request complexity as **Trivial**, **Standard**, or **Complex**.

    - **Trivial** — single-file edit, factual question with no implementation intent, or explicit user override. Proceed directly.
    - **Standard / Complex** — your FIRST tool call MUST be `Task(subagent_type="jg-planner", ...)`.

    **Pipeline Order**

    - Plan: jg-subplanner (or planner gives direct scope for trivial tasks)
    - Implement: jg-worker
    - Verify: jg-tester (Phase 1 + Phase 2 per project)
    - Review: jg-reviewer (only after tester PASS)
    - Ship: jg-git (only after reviewer PASS)
    - On failure: jg-debugger classifies; planner routes fix_target → worker, plan_defect → subplanner, escalate → human/architect

## jg-commit-conventions

**Frontmatter:** `description: Commit and PR conventions`, `alwaysApply: false`

**Purpose:** Standardizes commit messages, branch names, and PR practices. Uses Conventional Commits with issue ID as scope.

??? note "Key sections"
    **Message Format**

    ```
    feat(ISSUE-123): short description
    fix(ISSUE-456): short description
    docs(ISSUE-202): update README
    ```

    **Branch and PR**

    - Branch prefix: `feature/`, `fix/`, `chore/`, `spike/`. Lowercase, hyphen-separated. One issue per branch.
    - PR: title from primary commit; body with Summary and Test plan; reference issue(s).
    - Agents may open PRs; only a human may merge. No force push, no skip hooks.

## jg-issue-workflow

**Frontmatter:** `description: Issue-as-source-of-truth and start/completion workflow`, `alwaysApply: false`

**Purpose:** Treats the issue as the canonical spec. Ensures acceptance criteria exist before implementation and that completion is reported back.

??? note "Key sections"
    **Core Policy**

    - The issue is the authoritative spec. Do not rely on a duplicate spec file that can drift.
    - If the issue and other docs disagree, follow the issue.

    **Start of Work**

    1. Read the issue (body and comments). Confirm acceptance criteria exist and are unambiguous.
    2. Apply project status (e.g. label `status:in-progress`). Create `.pipeline/<issue-id>/` when the pipeline starts.
    3. Do not start implementation without clear AC.

    **Completion**

    - When the pipeline finishes: post execution report to the issue, apply done status, reference the issue in commit and PR.

## jg-pr-review

**Frontmatter:** `description: PR review categories and decision rules`, `alwaysApply: false`

**Purpose:** Defines finding categories (Blocker, Concern, Nit) and merge decision rules for jg-reviewer and human reviewers.

??? note "Key sections"
    **Finding Categories**

    | Category | Meaning | Merge impact |
    |----------|---------|--------------|
    | Blocker | Correctness, safety, or CI failure | Must fix before merge |
    | Concern | Quality, maintainability, incomplete coverage | Should fix before merge |
    | Nit | Style, naming, optional improvement | Author's discretion |

    **Decision Rules**

    - **APPROVE**: only when all remaining findings are Nits.
    - **REQUEST CHANGES**: when any Blocker or Concern is unresolved.
    - Do not post APPROVE with conditions; either request changes or approve.

## jg-tier-routing

**Frontmatter:** `description: Complexity classification and tiered agent routing`, `alwaysApply: true`

**Purpose:** Classifies tasks as Trivial, Standard, or Complex and maps each to the correct agent tier (fast, standard, high). Expert tier only.

??? note "Key sections"
    **Complexity Classification**

    - **Trivial** — 1-2 files, single domain, no new abstractions, no security implications
    - **Standard** — 3+ files, or cross-domain, or requires tests across modules
    - **Complex** — safety-critical code, new abstractions, architectural changes, real-time systems, concurrency

    **Tier Assignment**

    | Complexity | Subplanner | Worker | Tester | Reviewer | Debugger |
    |-----------|------------|--------|--------|----------|----------|
    | Trivial | (skip) | jg-worker-fast | jg-tester-fast | jg-reviewer-fast | (skip) |
    | Standard | jg-subplanner | jg-worker | jg-tester | jg-reviewer | jg-debugger |
    | Complex | jg-subplanner-high | jg-worker-high | jg-tester | jg-reviewer-high | jg-debugger-high |

    **Escalation**

    When any agent returns `status: escalate`: upgrade to the next tier, re-dispatch, do NOT count as retry. If already at high tier, escalate to human.
