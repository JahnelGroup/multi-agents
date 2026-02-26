# JG rules

| File | Purpose | alwaysApply |
|------|---------|-------------|
| jg-planner-first.mdc | Delegate multi-step work to jg-planner; pipeline order; exempt cases | false (enable when using jg- pipeline) |
| jg-commit-conventions.mdc | Conventional commits, branch/PR policy | false |
| jg-issue-workflow.mdc | Issue as source of truth; start/completion workflow; long-running spec | false |
| jg-pr-review.mdc | PR review categories (Blocker/Concern/Nit), APPROVE vs REQUEST CHANGES, body format | false |

Set `alwaysApply: true` on **jg-planner-first.mdc** when this pipeline is your default orchestration. Use **jg-issue-workflow** and **jg-pr-review** when issues and GitHub PRs are part of your workflow.
