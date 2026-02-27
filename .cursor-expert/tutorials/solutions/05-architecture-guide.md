# Architecture Proposal -- Solution Guide

This is a portfolio exercise. The exemplar in `outputs/05-architecture.md` shows a strong response. Key evaluation criteria:

## Required sections (all 7 must be present)

1. **Agent Inventory**: Table with 10+ agents including tiered variants and custom domain agents (e.g., `team-security-scanner`). Must show model, tier, role, and readonly flag.

2. **Pipeline Flow**: Mermaid diagram showing tiered routing from planner through git, including the security scanning stage and failure/retry paths.

3. **Tier Routing Rules**: Decision criteria for trivial/standard/complex. Must include the PCI-DSS override rule (always high tier for payment-related code).

4. **Cost Projections**: Math showing 20 PRs/week × 4.3 weeks with 60/25/15 mix. Must total under $50/month. Show per-tier cost breakdown.

5. **Monitoring Strategy**: At least 3 metrics (retry rate, escalation rate, cost per issue, PR cycle time). Include alerting thresholds.

6. **Escalation Policy**: Automatic tier upgrades, human escalation triggers, max retry counts per tier.

7. **Rollback Plan**: Per-stage failure handling explaining what state exists and how to recover.

## Scoring signals for strong answers

- Cost projections use realistic per-invocation costs, not made-up numbers
- PCI-DSS override is clearly articulated as a mandatory routing constraint
- Monitoring metrics are tied to specific alerting thresholds
- Rollback plan acknowledges that no git state exists until the git stage
- Custom agents serve a domain-specific purpose, not generic padding
