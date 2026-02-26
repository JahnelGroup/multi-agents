# Exercise 05: Architecture Proposal (Portfolio)

## Objective

Portfolio exercise. Design a multi-agent CI/CD pipeline for a fintech company with strict compliance requirements.

## Required Reading

- [Expert README](../../README.md) -- entire document
- [Expert walkthrough routing log](../../walkthrough/routing-log.md) -- routing decision documentation
- [Expert walkthrough cost summary](../../walkthrough/cost-summary.md) -- cost analysis format

## Scenario

**Client**: FinSecure, a fintech startup building a payment processing platform.

**Requirements**:
- All code changes must pass security scanning before merge
- Compliance audit trail required for every PR (who reviewed, what was checked)
- PCI-DSS relevant changes must use high-tier agents only
- Cost budget: $50/month for agent pipeline usage
- Team size: 4 developers, ~20 PRs/week
- Mix: 60% trivial (config, docs), 25% standard (features), 15% complex (payment flows)

## Tasks

Produce an architecture document with these 7 required sections:

### 1. Agent Inventory
Table of all agents with tier assignments, models, and roles. Must include at least: planner, subplanner, worker (3 tiers), tester (2 tiers), reviewer (3 tiers), debugger, git, plus a custom `team-security-scanner` agent.

### 2. Pipeline Flow
Mermaid diagram showing the full pipeline with tier routing, including the security scanning stage.

### 3. Tier Routing Rules
Decision criteria for trivial/standard/complex classification, with PCI-DSS override rule (always high tier for payment-related changes).

### 4. Cost Projections
Monthly cost estimate based on 20 PRs/week with the stated mix (60/25/15). Show the math. Must fit within $50/month.

### 5. Monitoring Strategy
Metrics to track: retry rate, escalation rate, cost per issue, PR cycle time. Alerting thresholds (e.g., escalation rate > 15% triggers review of classification criteria).

### 6. Escalation Policy
When and how to escalate between tiers and to humans. Maximum retry counts per tier.

### 7. Rollback Plan
How to handle agent failures at each stage without losing work.

## Output

Write to `tutorials/outputs/05-architecture.md`.

## Validation

```bash
python3 .cursor-expert/tutorials/verify.py --exercise 05
```

Checks: file exists, all 7 section headings present, Agent Inventory has a markdown table, Pipeline Flow has a mermaid block, Cost Projections has dollar amounts, Monitoring Strategy mentions 3+ metrics.

## Reflection

- How would you present this to a non-technical stakeholder?
- What's the biggest risk in this architecture?
- How would you onboard the FinSecure team to use this pipeline?
