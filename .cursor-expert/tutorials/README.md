# Expert Tutorials

Design and deployment exercises that test your ability to architect multi-agent systems, route to tiered subagents, handle escalation, analyze costs, and produce architecture documentation.

## Prerequisites

- Python 3.10+ (for verify.py, schema.py, check.py)
- Node.js 18+ (for sandbox project)
- Practitioner exercises 01-05 completed (sandbox has auth feature)
- `.cursor-expert/` content available for reference

## Cursor Documentation

These exercises build on concepts covered in the official Cursor documentation:

| Topic | Link | Exercises |
|-------|------|-----------|
| Custom agents & tiers | [Custom Agents - Cursor Docs](https://docs.cursor.com/agent/custom-agents) | 01, 02, 03, 04, 05, 07 |
| Feature development | [Developing Features - Cursor Learn](https://cursor.com/learn/creating-features) | 02 |
| Debugging workflows | [Finding and Fixing Bugs - Cursor Learn](https://cursor.com/learn/finding-and-fixing-bugs) | 03 |
| Code review patterns | [Reviewing and Testing Code - Cursor Learn](https://cursor.com/learn/reviewing-and-testing-code) | 05 |
| Rules (.mdc) | [Rules - Cursor Docs](https://docs.cursor.com/context/rules) | 01, 05, 06 |
| Skills (SKILL.md) | [Agent Skills - Cursor Docs](https://docs.cursor.com/context/skills) | 02, 04, 06, 07 |
| Agent customization | [Customizing Agents - Cursor Learn](https://cursor.com/learn/customizing-agents) | 05, 06 |

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
| 01 | [Classify Complexity](../../docs/expert/exercises/01-classify-complexity.md) | Analytical | 5 classifications in JSON |
| 02 | [Tiered Pipeline](../../docs/expert/exercises/02-tiered-pipeline.md) | Hands-on | 3 NOTIF issues through tiered pipeline |
| 03 | [Escalation Patterns](../../docs/expert/exercises/03-escalation-patterns.md) | Hands-on | Escalation flow with history |
| 04 | [Cost Analysis](../../docs/expert/exercises/04-cost-analysis.md) | Analytical | 3 strategies compared |
| 05 | [Architecture Proposal](../../docs/expert/exercises/05-architecture-proposal.md) | Portfolio | 7-section architecture document |
| 06 | [Rules & Skills Design](../../docs/expert/exercises/06-rules-and-skills-design.md) | Portfolio | Configuration design for tiered system |
| 07 | [Benchmark Review](../../docs/expert/exercises/07-benchmark-review.md) | Hands-on | Benchmark snapshot + evaluation report |
| 08 | [Agent Evaluation](../../docs/expert/exercises/08-agent-evaluation.md) | Portfolio | Quality rubrics for plan and review artifacts |

## Verification

```bash
python3 .cursor-expert/tutorials/verify.py --exercise 01   # single exercise
python3 .cursor-expert/tutorials/verify.py --all          # all 8 exercises
```

## Claude Code

Analytical exercises (01, 04, 05) are IDE-agnostic. For hands-on exercises (02, 03), replace `Task` calls with sequential prompting to tiered models. The artifacts and validation commands are identical.
