# Expert Tutorials

Design and deployment exercises that test your ability to architect multi-agent systems, route to tiered subagents, handle escalation, analyze costs, and produce architecture documentation.

## Prerequisites

- Python 3.10+ (for verify.py, schema.py, check.py)
- Node.js 18+ (for sandbox project)
- Practitioner exercises 01-05 completed (sandbox has auth feature)
- `.cursor-expert/` content available for reference

## Critical Requirement: Tiered Subagent Routing

Exercises 02-03 MUST use the correct tiered subagents. As the planner, you route to the appropriate tier:

| Complexity | Subplanner | Worker | Tester | Reviewer |
|-----------|------------|--------|--------|----------|
| Trivial | (skip) | jg-worker-fast | jg-tester-fast | jg-reviewer-fast |
| Standard | jg-subplanner | jg-worker | jg-tester | jg-reviewer |
| Complex | jg-subplanner-high | jg-worker-high | jg-tester | jg-reviewer-high |

## Exercises

| # | Title | Type | Tests |
|---|-------|------|-------|
| 01 | [Classify Complexity](exercises/01-classify-complexity.md) | Analytical | 5 classifications in JSON |
| 02 | [Tiered Pipeline](exercises/02-tiered-pipeline.md) | Hands-on | 3 NOTIF issues through tiered pipeline |
| 03 | [Escalation Patterns](exercises/03-escalation-patterns.md) | Hands-on | Escalation flow with history |
| 04 | [Cost Analysis](exercises/04-cost-analysis.md) | Analytical | 3 strategies compared |
| 05 | [Architecture Proposal](exercises/05-architecture-proposal.md) | Portfolio | 7-section architecture document |

## Verification

```bash
python3 .cursor-expert/tutorials/verify.py --exercise 01
python3 .cursor-expert/tutorials/verify.py --all
```

## Claude Code

Analytical exercises (01, 04, 05) are IDE-agnostic. For hands-on exercises (02, 03), replace `Task` calls with sequential prompting to tiered models. The artifacts and validation commands are identical.
