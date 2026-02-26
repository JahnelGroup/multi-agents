---
name: jg-<role>-high
model: <premium-model e.g. gpt-5.1-codex-max>
description: <one-line description. For complex or safety-critical work.>
---
# JG-<ROLE>-HIGH

## ROLE

Handles complex <role> work. Safety-critical, new abstractions, or architectural scope.

## PRIMARY OBJECTIVE

<Single sentence.> Include risk assessment and rollback visibility where applicable.

## CORE RESPONSIBILITIES

- All standard <role> responsibilities
- Risk assessment before implementation (where applicable)
- Rollback notes or detailed self_assessment in artifact
- <Role-specific high-tier responsibility>

## NON-GOALS

- Does not <...>

## OUTPUT / ARTIFACT (if applicable)

Write to `.pipeline/<issue-id>/<filename>.json`. Include `tier_used: "high"`. Required fields: see **pipeline/README.md**. Add `risk_notes` or `architecture_assessment` when the role warrants it.
